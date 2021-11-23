from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer
from sinling import word_splitter
import re

tokenizer = SinhalaTokenizer()
es = Elasticsearch()
app = Flask(__name__)
index_name= "lk-pm-en"

# Sinhala context identifiers for the query.
pmKeywords = ["මන්ත්‍රීවරයා", "මන්ත්‍රීවරයා", "මැතිතුමා", "මැති", "ගරු", "පා.ම."]
locationKeywords = ["ප්‍රදේශයේ", "දිස්ත්‍රික්කයේ", "දිස්ත්‍රික්කය", "ප්‍රදේශය"]
yearKeywords = ["වසරේ", "වර්ෂය", "වසර", "වර්ෂයේ", "උපන්", "ඉපදුන"]
committeeKeywords = ["කමිටුව" "කමිටුවේ"]
partyKeywords = ["පක්ෂයේ", "පක්ෂය", "සන්ධානය", "සන්ධානයේ"]
# English context identifiers for the query.
enPmKeywords = ["member", "member", "mr.", "mrs.", "hon.", "mp"]
enLocationKeywords = ["area", "district"]

class QueryProcessor:
    def __init__(self):
        print("Initializing Query Processor")

    # Apply preprocessing to the query.
    def preprocessQuery(self, query):

        # Tokenize the query using  sinling.
        tokens = tokenizer.tokenize(query)
        boost_list, modified_query = self.getPriorities(tokens, query)
        if(boost_list):
            return self.boostQuery(modified_query, boost_list)
        else:
            return self.defaultQuery(modified_query)

    # Find the priorities in the query and prepare priority list for fields.
    def getPriorities(self, tokens,query):
        field_priorities = {}
        for token in tokens:
            if(token.isalpha()):
                print("English detected", token)
                if(token.lower() in enPmKeywords):
                    field_priorities['name_en'] = 2.0
                    query = self.removeContexIdentifiers(query, [token])

                if(token.lower() in enLocationKeywords):
                    field_priorities['electoral_en'] = 2.0
                    query = self.removeContexIdentifiers(query, [token])
            else:
                splitted_words = word_splitter.split(token)
                # Check whether the token or splitted word appears in any of the defined context identifiers.
                if(token in pmKeywords or splitted_words['affix'] in pmKeywords or splitted_words['base'] in pmKeywords):
                    field_priorities['name'] = 2.0
                    query = self.removeContexIdentifiers(query, [token, splitted_words['base'], splitted_words['affix']])

                if(token in locationKeywords or splitted_words['affix'] in locationKeywords or splitted_words['base'] in locationKeywords):
                    field_priorities['electoral'] = 2.0
                    query = self.removeContexIdentifiers(query, [ token, splitted_words['affix'], splitted_words['base']])

                if(token in yearKeywords or splitted_words['affix'] in yearKeywords or splitted_words['base'] in yearKeywords):
                    field_priorities['dob'] = 2.0
                    query = self.removeContexIdentifiers(query, [token, splitted_words['base'], splitted_words['affix']])

                if(token in committeeKeywords or splitted_words['affix'] in committeeKeywords or splitted_words['base'] in committeeKeywords):
                    field_priorities['committees'] = 2.0

                if(token in partyKeywords or splitted_words['affix'] in partyKeywords or splitted_words['base'] in partyKeywords):
                    field_priorities['party'] = 2.0
        
        boost_list = []
        if(field_priorities.keys()):
            for field in field_priorities.keys():
                boost_list.append("{0}^{1}".format(field, field_priorities[field]))
            print(boost_list)
        return boost_list, query

    # Remove priority context identifier tokens from the query.
    def removeContexIdentifiers(self, query, tokens):
        for token in tokens:
            query = query.replace(token," ")
        print(query)
        return query

    # Build the default query, if boosting is not present.
    def defaultQuery(self,query):
        if(query.strip()==""):
            body =  {
                "query": {
                    "match_all": {}
                }
            }
        else:
            body =  {
                "query": {
                    "multi_match": {
                        "query": query,
                        "operator": "and"
                    }
                }
            }
        return body

    # Build query if boosting is present.
    def boostQuery(sef, query, boost_list):
        if(query.strip()==""):
            body =  {
                "query": {
                    "match_all": {}
                }
            }
        else:
            body =  {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": boost_list
                    }
                }
            }
        return body

@app.route('/', methods=['GET', 'POST'])
def home():
    results = None

    if request.method=="POST":
        form = request.form
        query = form['search']
        print("Query:",query)

        qpr = QueryProcessor()

        exactMatchQuery = re.search("[\"\']*[\"\']", query)

        if exactMatchQuery:
            body = {
                "query": {
                    "match_phrase":{
                        "name": query
                    }
                }
            }
        else:
            ppdquery = qpr.preprocessQuery(query)
            body = ppdquery

        response = es.search(index=index_name, body=body)
        count = response['hits']['total']['value']
        print(response)
        pm_list = []
        for result in response['hits']['hits']:
            pm_list.append(result['_source'])

        results = {'count':count, 'data':pm_list, 'query':query}

    # return jsonify(response)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
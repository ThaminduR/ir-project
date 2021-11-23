# Search Engine for Sri Lankan MPs.

A project carried out under the Data Mining and Information Retrieval Module.

This project contains four parts

1. Data Scraping
2. Transliterate data into Sinhala
3. Building a index using ElasticSearch
4. Flask Application

## Data Scraping
- Data Source: https://www.parliament.lk/
- Missing data values were replaced by `N/A`.
- A single missing value in the date of birth field was filled manually.
- Data files are located in the data/ directory with the stats related to missing information.
- Scraping scripts are located in the scrapy directory.
- Scraped data contains following fields,
    1. Name
    2. Date of birth 
    3. Civil status
    4. Religion
    5. Party
    6. Electoral district
    7. Email
    8. Served committees

## Transliterate data into Sinhala

- Scraped data was transliterated into Sinhala using `mtranslate` pip package (`pip install mtranslate`).
- `N/A` values were replaced by `දත්ත නොමැත` ("No Data" in Sinhala).
- Values in the email section were kept as it is.

## Indexing using ElasticSearch

- The settings, mapping for the created index are located in the elasticsearch/mapping.json file.
- Custom analyzers were introduced for both Sinhala and English languages.
- icu tokenizer is used for the Sinhala text and standard, lowercase tokenizer is used for the English text.
- Several character mappings were also introduced during both indexing time and query time. (. ' " @ characters were mapped to a whitespace character.)
- edge_ngram_filter was also used in both Sinhala and English analyzers.
- Indexing was done with all the fields in Sinhala and `name` and `electoral` in English.

## Flask Application

- A simple flask application was created for the searching. Retreived data is displayed in a table.

![Directory of Members of Parliment](images\ui.png)

# Features

- Supports  searching  by  `name`,  `date  of  birth`,  `civil status`,  `religion`,  `party`, ` electoral  district`,`email`, `served committees`, `career`.
- Supports query boosting by identifying specific fields related to query using synonyms and applying boosting to the identified fields. This uses [sinling tokenizer](https://github.com/ysenarath/sinling) for the tokenizing and word splitting. A set of predefined lists are maintained to identify the context of the query.
- Supports bilingual search for `name` and `electoral` fields. Code-mixed queries are also supported.

# Query Preprocessing

<img src="images\flow.png" width="500">


# Project Structure

- elasticsearch - Contains settings and mapping json for the index creation and python script for updating index with the data.
- flask - Contains code for the flask app and app.py contains the query processing logic.
- images - Images added in the README.md
- irpScrape - Contains scrapy scripts, spiders and scraped data and translated data.
# Setting Up and Running the Project

- Install the required packages using requirements.txt.

1. Data Scraping - In the irpScrape folder, run `scrapy crawl pm` to crawl the data from the parliment website.
2. Translation - Run the `translate.py` script in the translate-scripts folder.
3. Creating Index - Start elasticsearch and create an index using the `mapping.json` given in elasticsearch folder.
4. Add Data to Index - Run the `index_dat.py` script to add data into the index.
5. Start the Flask App - Run `python run.py` inside the flask folder to start the flask app.


Note: The data crawled from the parliment website is used only for educational purposes only.


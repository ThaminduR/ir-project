import scrapy
import string
import ast
import json

class PMSpider(scrapy.Spider):
    name = "pm"
    stats = {"name":0, "dob":0, "civil":0, "religion":0, "party":0, "electoral":0, "email":0, "committees":0, "total_row_count":0}
    id_list = []
    people = []
    pms_lk = 'https://www.parliament.lk/members-of-parliament/index2.php?option=com_members&task=all&tmpl=component&letter=%s'
    member_link = 'https://www.parliament.lk/members-of-parliament/directory-of-members/viewMember/%s'

    def start_requests(self):
        for letter in string.ascii_uppercase:
            yield scrapy.Request(url=self.pms_lk%letter, callback=self.parse_ids)
        if len(self.id_list)==0:
            self.error("Empty id_list")
        else:
            for id in self.id_list:
                yield scrapy.Request(url=self.member_link%id, callback=self.parse_member)

    def parse_ids(self, response):
        names_list = ast.literal_eval(response.body.decode('utf-8'))
        for name_dict in names_list:
            self.stats["total_row_count"] += 1
            self.id_list.append(name_dict['mem_intranet_id'])

    def parse_member(self, response):
        person = {}
        name = response.xpath('/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/h2/text()').get()
        name = name.split(',')[0].strip()
        person['name'] = name

        table_rows = response.xpath('//*[contains(@class,"mem_profile")]//tr')
        for table_row in table_rows:
            # Date of Birth.
            dob = table_row.re(r"<span>Date of Birth</span> : \d*-\d*-\d*")
            if(len(dob)!=0):
                dob = dob[0].split(":")[-1].strip()
                person["dob"] = dob

            # Civil Status.
            civil = table_row.re(r"<span>Civil Status</span> : \w*")
            if(len(civil)!=0):
                civil = civil[0].split(":")[-1].strip()
                person["civil"] = civil

            # Religion
            rel = table_row.re(r"<span>Religion</span> : \w*")
            if(len(rel)!=0):
                rel = rel[0].split(":")[-1].strip()
                person["religion"] = rel

            # Party
            party = table_row.re(r"Party</div>")
            if(len(party)!=0):
                party = table_row.re(r">.*</a>")[0][1:-4]
                person["party"] = party

            # Electoral District
            ed = table_row.re(r"Electoral District / National List</div")
            if(len(ed)!=0):
                ed = table_row.re(r".*</td>")[0]
                person["electoral"] = ed[:-5].strip()

        # Email
        email = response.xpath('/html/body').re(r"\w*@parliament.lk")
        if(len(email)!=0):
            person["email"] = email[0].strip()
        
        
        committees = response.xpath('//div[@class="top-mp-detail-4"]/div/div/ul/li/a/text()').extract()
        if(len(committees)!=0):
            person["committees"] = committees

        for att in ["dob", "civil", "religion", "party", "electoral", "email", "committees"]:
            try:
                person[att]
            except:
                self.stats[att] +=1
                person[att] = "N/A"

        self.people.append(person)
        
        with open('data/pm-data.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.people))

        with open("data/stats.json", "w") as f:
            f.write(json.dumps(self.stats))



        
    
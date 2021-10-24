import json
from mtranslate import translate

json_file = open("pm-data.json", "r", encoding="utf-8")
data = json.load(json_file)

people = []
attrs = ["name", "dob", "civil", "religion", "party", "electoral", "email"]

count = 0
for person in data:
  si_person= {}

  for att in attrs:
    if((att=="dob") or (att=="email")):
      si_person[att] = person[att]
      continue
    if(person[att]== "N/A"):
      si_person[att] = "දත්ත නොමැත"
    else:
      si_person[att] = translate( person[att].lower(), 'si', 'en')
  people.append(si_person)
  count += 1
  print("{:0.2f}% Completed".format((count/225)*100))
  

with open('data/pm-si-data.json', 'w', encoding='utf8') as f:
    f.write(json.dumps(people, ensure_ascii=False))
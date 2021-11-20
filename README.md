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
- Data files are located in the data/ directory with the stats related to missing information.
- Scraping scripts are located in the scrapy directory.

## Transliterate data into Sinhala

- Scraped data was transliterated into Sinhala using `mtranslate` pip package (`pip install mtranslate`).
- `N/A` values were replaced by `දත්ත නොමැත` ("No Data" in Sinhala).
- Values in the email section were kept as it is.
- A single missing value in the date of birth field was filled manually.

## Indexing using ElasticSearch

- The settings, mapping for the created index are located in the elasticsearch/mapping.json file.
- icu tokenizer is used for the Sinhala text analyzing and standard lowercase tokenizer is used for the English text.
- Several character mappings were also introduced during both indexing time and query time. (. ' " @ characters were mapped to a whitespace character.)

## Flask Application

- A simple flask application was created for the searching. 
- TODO: Rule based classification and more complex query preprocessing.


# Setting Up and Running the Project

- Install the required packages using requirements.txt.

1. Data Scraping - In the irpScrape folder, run `scrapy crawl pm` to crawl the data from the parliment website.
2. Translation - Run the `translate.py` script in the translate-scripts folder.
3. Creating Index - Start elasticsearch and create an index using the `mapping.json` given in elasticsearch folder.
4. Add Data to Index - Run the `index_dat.py` script to add data into the index.
5. Start the Flask App - Run `python run.py` inside the flask folder to start the flask app.


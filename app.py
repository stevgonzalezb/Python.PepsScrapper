import requests
import configparser
import os
from bs4 import BeautifulSoup
import pandas as pd

config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

BASE_URL = config['config']['base_url']
COUNTRIES = config['config']['countries'].split(';')
USER_AGENT = config['config']['user_agent']
CSV_PATH = config['config']['csv_path']
SEPARATOR = config['config']['separator']


def get_html(country):
    url = BASE_URL + country
    headers = {"User-Agent": USER_AGENT}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def process_data():
    output_data= []
    
    for country in COUNTRIES:
        values = []
        
        page_content = get_html(country)
        html_data = page_content.find("div",{"class":"free-form-content__content wysiwyg-wrapper"})

        for value in html_data:
            if value.name == 'p' or value.name == 'h3':
                values.append(value)

        for cur, nxt in zip (values, values [1:] ):
            if cur.name == 'h3' and nxt.name == 'p':
                name = nxt.text.strip()
                title = cur.text.strip()
                output_data.append([country, name, title])

            if cur.name == 'h3' and nxt.name == 'h3':
                name = 'N/A'
                title = cur.text.strip()
                output_data.append([country, name, title])

    return output_data

data = process_data()
df = pd.DataFrame(data, columns = ['Country', 'Name', 'Title'])

df.to_csv(CSV_PATH, sep=SEPARATOR, index=False)

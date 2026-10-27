import requests
import xml.etree.ElementTree as ET
from psycopg2.extras import execute_values
from datetime import datetime

from db_utils import load_data

def get_cbr_rates():
    url = "http://www.cbr.ru/scripts/XML_daily.asp?"
    response = requests.get(url)
    response.encoding = "windows-1251"
    text = response.text
    
    root = ET.fromstring(text)
    
    rate_date = datetime.strptime(root.get('Date'), '%d.%m.%Y').date()
    currency = []
    # print(rate_date)
    for valute in root.findall('Valute'):
        char_code = valute.find('CharCode').text
        nominal = int(valute.find('Nominal').text)
        name = valute.find('Name').text
        value = float(valute.find('Value').text.replace(',', '.')) 
        currency.append((rate_date.strftime('%Y-%m-%d'), char_code, nominal, name, value))
    return currency


def load_to_db(currency):
    load_data(
        table_name='raw_cbr_currency',
        columns=['rate_date', 'char_code', 'nominal', 'name', 'value'],
        data=currency,
        conflict_target='rate_date, char_code'
    )

if __name__ == "__main__":
    cbr_rates = get_cbr_rates()
    load_to_db(cbr_rates)
    
# Import the required libraries
import requests
from bs4 import BeautifulSoup
import json
import datetime
import pytz
import time
import os, sys
import boto3

# finding the path to the python installation on the EC2 instance
path = os.path.dirname(sys.executable)
print(path)

# make sure s3 bucket can be used
bucket_name = 'scrapeovfiets'
destination_file_key_data = 'ov_data.json'
destination_file_key_html = 'raw_data.json'

# Define the URL of the website and the user agent header
url = 'https://ovfietsbeschikbaar.nl/locaties'
header = {'User-agent': 'Mozilla/5.0'}
# Get the HTML code from the website and process it with BeautifulSoup
res = requests.get(url, headers=header)
res.encoding = res.apparent_encoding
source_code_0 = res.text  # make website html code readable as text

# Make information "extractable" using BeautifulSoup
soup0 = BeautifulSoup(source_code_0, 'html.parser')

# store the raw data in a dictionary
raw_data_hoofdlink = {'html': str(soup0)}

# Find the list of locations on the page and get the links to the OV-fiets stations
locatielijst = soup0.find('a', attrs={'name': 'Locatielijst'})
stations = [a['href'] for a in locatielijst.find_next('div').find_all('a', {'class': 'panel-block'})]

# Create a list of links to the OV-fiets stations
links = []
for station in stations:
    combined_link = "https://ovfietsbeschikbaar.nl" + station
    links.append(combined_link)

# Define the parse_website function to extract information from each OV-fiets station webpage
def parse_website(url):
    header = {'User-agent': 'Mozilla/5.0'}  # with the user agent, we let Python know for which browser version to retrieve the website
    request = requests.get(url, headers=header)
    request.encoding = request.apparent_encoding  # set encoding to UTF-8
    source_code = request.text  # make website html code readable as text

    # Make information "extractable" using BeautifulSoup
    soup = BeautifulSoup(source_code, 'html.parser')

    # Scrape the relevant information
    station = soup.find(class_='title has-text-weight-bold').get_text()
    totaal = soup.find(title='Schatting op basis van de laaste drie maanden').get_text(strip=True)
    if soup.find(class_="grafiek-overlay").get_text(strip=True) == 'geen actueledata beschikbaar':
        beschikbaar = 'Geen actuele data beschikbaar'
    elif soup.find("div", {"class": "grafiek-overlay"}).find("span", {"class": "badge"})['data-badge'] == '!':
        beschikbaar = 'Vertraging in de data'
    else:
        beschikbaar = soup.find('td', string='Nu beschikbaar').find_next_sibling('td').get_text(strip=True)
    soort = soup.find('td', string='Type stalling').find_next_sibling('td').get_text(strip=True)
    adres = soup.find(class_='table is-narrow is-fullwidth').find('td').get_text()
    if adres.startswith('Adres:'):
        adres = adres.replace('Adres:', '')
    else:
        adres = 'Onbekend'

    # extract current date and time
    current_datetime = datetime.datetime.now(pytz.timezone('Europe/Amsterdam'))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

    # store the information in a dictionary
    data = {'date': formatted_datetime,
            'station': station,
    		'totaal': totaal,
    		'beschikbaar': beschikbaar,
        'type stalling': soort,
        'adres': adres}

    # store the raw data in a dictionary
    raw_data = {'date': formatted_datetime, 'html': str(soup)}

    return (data, raw_data)

# store the raw data of the html structure in a json file
f = open('raw_data.json', 'a', encoding='utf-8')
f.write(json.dumps(raw_data_hoofdlink))
f.write('\n')  # new line to separate objects
f.close()

f = open('raw_data.json', 'a', encoding='utf-8')
for link in links:
    raw_data = parse_website(link)[1]
    f.write(json.dumps(raw_data))
    f.write('\n')  # new line to separate objects
f.close()

# store the scraped data in a json file
f = open('ov_data.json', 'a', encoding='utf-8')
for link in links:
    data = parse_website(link)[0]
    f.write(json.dumps(data))
    f.write('\n')  # new line to separate objects
f.close()

# Create an S3 client
s3 = boto3.client('s3')

# Upload the file to S3
s3.put_object(Body=open('ov_data.json', 'rb'), Bucket=bucket_name, Key=destination_file_key_data)
s3.put_object(Body=open('raw_data.json', 'rb'), Bucket=bucket_name, Key=destination_file_key_html)

time.sleep(1)
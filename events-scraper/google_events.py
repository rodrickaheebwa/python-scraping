import requests
from bs4 import BeautifulSoup
import csv

def get_soup(url):
    headers = {
        "accept-language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_last_event(url):
    soup = get_soup(url)
    try:
        event_container = soup.find('div', class_ = 'mR2gOd')
        events_cards = event_container.find_all('a', class_ = 'ct5Ked klitem-tr PZPZlf')
        return 'https://www.google.com/' + events_cards[-1]['href']
    except:
        return False


def get_events(url):
    soup = get_soup(url)
    events = []
    event_container = soup.find('div', class_ = 'mR2gOd')
    events_cards = event_container.find_all('a', class_ = 'ct5Ked')
    for event_card in events_cards:
        event = {}
        event_info = event_card.find('div', class_ = 'gEYEQc x5W9xd qYvl9c klitem')
        name = event_info.find('div', class_ = 'bVj5Zb FozYP').text
        location = event_info.find('div', class_ = 'TCYkdd FozYP').find('span').text
        date = event_info.find('div', class_ = 't3gkGd').find('div').text
        try:
            time = event_info.find('div', class_ = 't3gkGd').find('div', class_ = 'oonKPc').text
        except:
            time = 'Not available'
        event['Name'] = name
        event['Location'] = location
        event['Date'] = date
        event['Time'] = time
        events.append(event)
    return events

def write_to_csv(folder, city, data):
    city = city.replace(' ', '-')
    csv_path = folder + '/' + city + '-events.csv'
    with open(csv_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def main():
    city = input('Enter a city whose events you want: ')
    city = city.lower()
    url = 'https://www.google.com/search?q=events+in+' + city.replace(' ', '+')
    last_url = get_last_event(url)
    if last_url:
        events = get_events(last_url)
        write_to_csv('test', city, events)
    else:
        print('Events not found!')
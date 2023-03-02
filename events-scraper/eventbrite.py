# this doesn't work

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import shutil
import time

def get_soup(url):
    headers = {
        "accept-language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


PATH = 'driver/chromedriver.exe'
service_obj = Service(PATH)

city = input('Enter a city whose events you want: ')
city = city.lower()

driver = webdriver.Chrome(service=service_obj)

driver.get("https://www.eventbrite.com/")
input_box = driver.find_element(By.ID, 'locationPicker')
input_box.send_keys(city)
print('entered city name!')
input_box.send_keys(Keys.RETURN)
print('pressed enter!')

try:
    time.sleep(5)
    html = driver.page_source
    driver_soup = BeautifulSoup(html, 'html.parser')
    print('saved html!')
except:
    print('didn\'t go through try')
driver.quit()

def has_more_events(soup_):
    more_events = soup_.find('div', attrs={'data-testid': 'see-more-events'})
    try:
        events_url = more_events.find('a')['href']
        print('has more events!')
        return True, events_url
    except:
        print('doesn\'t have more events!')
        return False
    
has_more = has_more_events(driver_soup)

if has_more:
    soup = get_soup("https://www.eventbrite.com"+ has_more[1])
    print('requested more events!')
    print(soup)
else:
    events = driver_soup.find_all('div', class_ = 'feed__card-cell')
    print('found event cards!')
    time.sleep(5)
    print(len(events))
    for event in events:
        img = event.find('img', class_ = 'eds-event-card-content__image')['src']
        link = event.find('a', class_ = 'eds-event-card-content__action-link')['href']
        name = event.find('div', class_ = 'eds-event-card__formatted-name--is-clamped').text
        date = event.find('div', class_ = 'eds-event-card-content__sub-title').text
        location = event.find('div', class_ = 'card-text--truncated__one').text
        price = event.find('div', class_ = 'eds-event-card-content__sub eds-text-bm eds-text-color--ui-600 eds-l-mar-top-1').text
        organiser = event.find('div', class_ = 'eds-event-card__sub-content--organizer').text
        event_info = {
            name : name,
            date : date,
            location : location,
            price : price,
            organiser : organiser,
            img : img,
            link : link
        }
        print('\n', event_info.values())

# heavily delayed by slow network at the time.
# will need to be looked at back at the main library.
# as well as images in the csv
# project came to a painful end, couldn't proceed
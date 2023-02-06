import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import shutil

def get_item_data(driver, item_url):
    driver.get(item_url)
    title_btn = driver.find_element(By.CLASS_NAME, 'AssetTitle-module__showFullTitleButton___M5mSj')
    title_btn.click()
    
    title = driver.find_element(By.CLASS_NAME, 'AssetTitle-module__title___wdK3q').find_element(By.TAG_NAME, 'h1').text
    keywords = driver.find_element(By.CLASS_NAME, 'AssetTitle-module__keywords___JetF2').find_element(By.TAG_NAME, 'h2').text
    image = driver.find_element(By.CLASS_NAME, 'ImageCard-module__container___tsZo8').find_element(By.TAG_NAME, 'img').get_attribute('src')

    driver.quit()
    return {'title':title, 'keywords':keywords, 'image':image}

def create_keywords_file(download_path, title, keywords):
    filepath = download_path + '/' + title + '.txt'
    try:
        with open(filepath, 'w') as file:
            file.write(keywords)
        print(f'{filepath} keyword file created successfully!')
    except Exception as e:
        print(e)
        print('Could not create keyword file')

def download_image(download_path, title, img_url):
    file_path = download_path + '/' + title + '.jpg'
    try:
        with requests.Session().get(img_url, stream=True) as response:
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            print(f'{file_path} downloaded successfully!')
    except Exception as e:
        print(e)
        print('Could not download image')

def single_page_scraper(item_url):
    PATH = 'driver/chromedriver.exe'
    service_obj = Service(PATH)
    driver = webdriver.Chrome(service=service_obj)
    item_data = get_item_data(driver, item_url)
    create_keywords_file('test', item_data['title'], item_data['keywords'])
    download_image('test', item_data['title'], item_data['image'])
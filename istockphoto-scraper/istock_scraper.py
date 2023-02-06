import requests
from bs4 import BeautifulSoup
import os
from single_page_scraper import single_page_scraper
import concurrent.futures

def get_soup(url):
    headers = {
        "accept-language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_number_of_pages(results_url):
    soup = get_soup(results_url)
    pages = soup.find('section', class_ = 'PaginationRow-module__container___NNDjw').find('span', class_ = 'PaginationRow-module__lastPage___q1Bw1').text
    print(pages, 'pages found!')
    return int(pages)

def get_page_item_links(url):
    soup = get_soup(url)
    item_container = soup.find('div', class_ = 'GalleryItems-module__container___h2Tb5')
    items = item_container.find_all('div', class_ = 'MosaicAsset-module__galleryMosaicAsset___Nt_YP')
    base_url = 'https://www.istockphoto.com'
    item_links = map(lambda item : base_url + item.find('a')['href'], items)
    print('collected links on page: ', url)
    return list(item_links)

def get_all_pages_links(results_url):
    pages = get_number_of_pages(results_url)
    total_item_links = []
    for num in range(1, pages+1):
        url = results_url + '&page=' + str(num)
        page_links = get_page_item_links(url)
        total_item_links.extend(page_links)

    print('collected all pages links!')
    return total_item_links

def create_download_folder():
    try:
        os.mkdir('test')
        print('created download folder!')
    except:
        print('could not create download folder!')

# without threading
def main1():
    create_download_folder()
    base_url = 'https://www.istockphoto.com/search/2/image?phrase=business+and+finance'
    item_links = get_all_pages_links(base_url)
    for link in item_links:
        single_page_scraper(link)

# with threading
def main2():
    create_download_folder()
    base_url = 'https://www.istockphoto.com/search/2/image?phrase=business+and+finance'
    item_links = get_all_pages_links(base_url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(single_page_scraper, item_links)
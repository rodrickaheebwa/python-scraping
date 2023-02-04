from template_page_scraper import template_page_scraper
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import os

def get_soup(url):
    headers = {
        "accept-language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_links_in_page(url):
    soup = get_soup(url)
    items = soup.find_all('li', class_ = 'Z9wqao0i')

    template_links = []

    for item in items:
        content = item.find('a')
        title = content['title']
        link = content['href']
        template_links.append(link)

    return template_links

def get_number_of_pages(results_url):
    soup = get_soup(results_url)
    pagination = soup.find('div', class_ = 'hZFJ5g_b').find('div', class_ = 'ISXMDuuA')
    pages = int(pagination.text.strip().split(' ')[0])
    return pages

def get_all_results_links(results_url):
    pages = get_number_of_pages(results_url)
    total_template_links = []
    for num in range(1, pages+1):
        url = results_url + '/pg-' + str(num)
        page_links = get_links_in_page(url)
        total_template_links.extend(page_links)

    print('collected result links!')

    return total_template_links

def create_download_folder():
    try:
        os.mkdir('envato-stock-templates')
        print('created download folder!')
    except:
        print('could not create download folder!')

# without threading
def main1():
    create_download_folder()
    base_url = 'https://elements.envato.com/graphic-templates/print-templates+ux-and-ui-kits/saas/sort-by-latest'
    urls = get_all_results_links(base_url)
    for url in urls:
        template_page_scraper('https://elements.envato.com' + url)

# with threading
def main2():
    create_download_folder()
    base_url = 'https://elements.envato.com/graphic-templates/print-templates+ux-and-ui-kits/saas/sort-by-latest'
    urls = get_all_results_links(base_url)
    urls = list(map(lambda url : 'https://elements.envato.com' + url, urls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(template_page_scraper, urls)

main2()
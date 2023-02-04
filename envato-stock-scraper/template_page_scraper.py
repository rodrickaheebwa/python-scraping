import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import shutil
import threading

def get_soup(url):
    headers = {
        "accept-language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# get title, for file name
def get_title(url):
    soup = get_soup(url)
    title = soup.find('div', class_ = 'KKEJ7mjA').find('h1', class_ = 'D9ao138P').text.strip()
    unwanted = [' ', '\\', '\/', ':', '|', '<', '>', '"', '*', '?']
    for ch in unwanted:
        if ch in title:
            title = title.replace(ch, '-')
    return title

def get_tags(url):
    soup = get_soup(url)
    tag_containers = soup.find('div', class_ = 'eHTcIYYO').find('div', class_ = 'VxZcnVo8').find_all('div', class_ = 'm8ijx4MD')
    tags = map(lambda container : container.find('a', class_ = 'd0KA3Wtv').text, tag_containers)
    return list(tags)

def get_image_urls(url):
    image_urls = []
    soup = get_soup(url)
    main_image_url = soup.find('div', class_ = 'x0y_mRmw').find('div', class_ = 'MY02g2dt').find('img')['src']
    image_urls.append(main_image_url)
    try:
        other_image_urls = soup.find('div', class_ = 'XukJ15Cv').find_all('img')
        for img in other_image_urls:
            link = img['srcset']
            links = filter(lambda x: 'https' in x, link.split(' '))
            image_urls.append(list(links)[-1])
    except:
        pass
    
    return image_urls

# get tags, save them to file with title filename
def create_tag_file(download_path, url):
    filename = get_title(url)
    tags = get_tags(url)
    filepath = download_path + filename + '.txt'
    try:
        with open(filepath, 'w') as file:
            file.write(', '.join(tags))
        print(f'{filepath} tag file created successfully!')
    except Exception as e:
        print(e)
        print('Could not create tag file')

def download_template_image(file_path, img_url, get_session):
    session = get_session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    try:
        with session.get(img_url, stream=True) as response:
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            print(f'{file_path} downloaded successfully!')
    except Exception as e:
        print(e)
        print('Could not download image')

# get images (urls and download), save them with title filename, adding a number if they are multiple
def download_template_images(download_path, url, get_session):
    filename = get_title(url)
    images = get_image_urls(url)
    if len(images) == 1:
        download_template_image(download_path + filename + '.jpg', images[0], get_session)
    else:
        for num, image in enumerate(images):
            download_template_image(download_path + filename + f'-{num+1}' + '.jpg', image, get_session)


def template_page_scraper(template_url):
    download_path = 'envato-stock-templates/'
    thread_local = threading.local()
    def get_session():
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session
    create_tag_file(download_path, template_url)
    download_template_images(download_path, template_url, get_session)

def main():
    template_url = 'https://elements.envato.com/the-coffe-landing-page-coffee-6LRW4BV'
    template_page_scraper(template_url)
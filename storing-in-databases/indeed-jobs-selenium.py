from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def get_jobs_on_page(url):
    # placed driver inside this function to allow for the driver to open multiple pages
    service_obj = Service('driver/chromedriver.exe')
    driver = webdriver.Chrome(service=service_obj)
    jobs = []

    driver.get(url)
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, 'html.parser')

    container = soup.find('div', class_ = 'jobsearch-LeftPane')
    job_count = container.find('div', class_ = 'jobsearch-JobCountAndSortPane-jobCount').find('span').text
    jobs_cards = container.find('ul', class_ = 'jobsearch-ResultsList').find_all('div', class_ = 'cardOutline')

    for card in jobs_cards:
        job_title = card.find('h2', class_ = 'jobTitle').text
        company_name = card.find('span', class_ = 'companyName').text
        location = card.find('div', class_ = 'companyLocation').text

        estimated_salary_container = card.find('div', class_ = 'estimated-salary-container')
        salary_container = card.find('div', class_ = 'salary-snippet-container')

        if estimated_salary_container:
            c = estimated_salary_container
            salary = c.find('span', class_ = 'estimated-salary').find('span').text
        elif salary_container:
            c = salary_container
            salary = c.find('div', class_ = 'attribute_snippet').text
        else:
            salary = 'not available'

        job = { 'job_title': job_title, 'company_name': company_name, 'location': location, 'salary': salary }
        jobs.append(job)

    print('got jobs on page', url)
    return jobs

def get_jobs_on_many_pages(pages, base_url):
    total_jobs = []
    for num in range(pages):
        suffix = str(num) + '0'
        url = base_url + '&start=' + suffix
        jobs = get_jobs_on_page(url)
        total_jobs.extend(jobs)

    return total_jobs

def main():
    pages = 0
    base_url = 'https://www.indeed.com/jobs?q=New&fromage=3&sort=date'

    jobs = get_jobs_on_many_pages(pages, base_url)

    for job in jobs:
        print('title: ', job['job_title'])
        print('company_name: ', job['company_name'])
        print('location: ', job['location'])
        print('salary: ', job['salary'])
        print('\n')

if __name__ == '__main__':
    main()
# the proxy used is scrapeops (/proxy.scrapeops.io)

import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error

def get_soup(url):
    response = requests.get(
      url='https://proxy.scrapeops.io/v1/',
      params={
          'api_key': '', #insert api key
          'url': url, 
      },
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_jobs_on_page(url):
    jobs = []
    
    soup = get_soup(url)

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

def create_table(db):
    cur = db.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS jobs ( JobID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, company TEXT NOT NULL, location TEXT NOT NULL, salary TEXT NOT NULL);'''
    cur.execute(sql)

def insert_record(db, data):
    # one record at a time
    # avoid concatenating the collected data into your SQL statements as it carries several risks among which are exposure to SQL injections, messing up with the quotes
    sql = "INSERT INTO jobs (title, company, location, salary) VALUES (?, ?, ?, ?);"
    params = (data['job_title'], data['company_name'], data['location'], data['salary'])
    try:
        cur = db.cursor()
        cur.execute(sql, params)
        db.commit()
        print ("one record added successfully")
    except Error as e:
        print ("error in operation", e)
        db.rollback()

def insert_records(db, data):
    # many records at once
    # added list of tuples and not list of dictionaries because '%s' kept causing an error
    # which would have been VALUES (%(job_title)s, %(company_name)s, %(location)s, %(salary)s)
    # stackoverflow.com/questions/33636191/insert-a-list-of-dictionaries-into-an-sql-table-using-python
    data = list(map(lambda job : tuple(job.values()), data))
    sql = "INSERT INTO jobs (title, company, location, salary) VALUES (?, ?, ?, ?);"
    try:
        cur = db.cursor()
        cur.executemany(sql, data)
        db.commit()
        print ("all records added successfully")
    except Error as e:
        print ("error in operation", e)
        db.rollback()

def main():
    # uncomment to create database and table
    # db = sqlite3.connect(".\\test\\indeed.db")
    # create_table(db)

    pages = 1
    base_url = 'https://www.indeed.com/jobs?q=New&fromage=3&sort=date'

    jobs = get_jobs_on_many_pages(pages, base_url)

    # to populate the database at once
    # insert_records(db, jobs)

    # to populate the database one job at a time
    # for job in jobs:
    #     # print('title: ', job['job_title'])
    #     # print('company_name: ', job['company_name'])
    #     # print('location: ', job['location'])
    #     # print('salary: ', job['salary'])
    #     # print('\n')
    #     print(job)
    #     insert_record(db, job)
    
    # close the database connection
    # closing the connection in more than one places will cause a 'Cannot operate on a closed database' error
    # stackoverflow.com/questions/23045832
    # db.close()

if __name__ == '__main__':
    pass
    # main()
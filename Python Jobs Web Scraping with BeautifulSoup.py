# Scrapping from Python Related Jobs TimesJobs Webpage that are posted a few days ago
import datetime
import time
import csv
from bs4 import BeautifulSoup
import requests

# Create excel workbook and spreadsheet for storing scrapped data

def find_jobs():
    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='
    source = requests.get(url)
    source.raise_for_status() # check for source link validity
    soup = BeautifulSoup(source.text, 'html.parser')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for job in jobs:
        published_date = job.find('span', class_='sim-posted').span.text.replace('  ', '')
        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace('  ','').strip()
            application_link = job.header.h2.a['href']
            required_skills = job.find('span', class_='srp-skills').text.replace('  ', '').strip()
            # Add today's date to each time the program scraps data
            today = datetime.date.today()
            # Create csv file for storing scrapped data
            header = ['Today', 'Company Name', 'Required Skills', 'Application Link']
            data = [today, company_name, required_skills, application_link]
            with open('Job_info.csv', 'a+', newline='', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)


# writing a while loop that runs the code everyday and give me the latest result in my spreadsheet
if __name__ == "__main__":
    while True:
        find_jobs()
        waiting_time = 24
        print(f'waiting for {waiting_time} hours...')
        time.sleep(waiting_time*3600)


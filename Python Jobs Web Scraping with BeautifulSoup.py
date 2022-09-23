# Scrapping for Python Related Jobs TimesJobs Webpage that are posted a few days ago on a daily basis into a csv file

# Importing Libaries
import datetime
import time
import csv
from bs4 import BeautifulSoup
import requests


# A function that help find job which emcompases the beautifulsoup web scraping program
def find_jobs():
    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='
    source = requests.get(url)
    
    # check for source link validity
    source.raise_for_status() 
    soup = BeautifulSoup(source.text, 'html.parser')
    
    # Prettification of the hmtl code
    pretify_code = soup.prettify()
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
            
            # Ensure to first write 'w' the csv file and change code to append 'a+' subsequent data
            with open('Job_info.csv', 'a+', newline='', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)


# writing a while loop that runs the code everyday and give me the latest result into the csv file
if __name__ == "__main__":
    while True:
        find_jobs()
        waiting_time = 24
        print(f'waiting for {waiting_time} hours...')
        time.sleep(waiting_time*3600)


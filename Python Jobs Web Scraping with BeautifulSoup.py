import datetime
import time
import csv
from bs4 import BeautifulSoup
import requests
import smtplib
import schedule

# Function to send an email notification
def send_email():
    try:
        # Set up the email server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('your_email@gmail.com', 'your_app_password')  # Use an app password for security
        
        # Email content
        subject = "New Python Job Postings Available!"
        body = ("New Python job postings have been added. "
                "Check the attached CSV file for details.")
        
        msg = f"Subject: {subject}\n\n{body}"
        
        # Send the email
        server.sendmail('your_email@gmail.com', 'recipient_email@gmail.com', msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Function to find jobs
def find_jobs():
    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='
    source = requests.get(url)
    
    # Check for source link validity
    source.raise_for_status() 
    soup = BeautifulSoup(source.text, 'html.parser')
    
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for job in jobs:
        published_date = job.find('span', class_='sim-posted').span.text.replace('  ', '')
        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace('  ','').strip()
            application_link = job.header.h2.a['href']
            required_skills = job.find('span', class_='srp-skills').text.replace('  ', '').strip()
            today = datetime.date.today()
            
            # Create or append to CSV file
            header = ['Today', 'Company Name', 'Required Skills', 'Application Link']
            data = [today, company_name, required_skills, application_link]
            
            with open('Job_info.csv', 'a+', newline='', encoding='UTF8') as f:
                writer = csv.writer(f)
                # Write header only if file is new
                if f.tell() == 0:
                    writer.writerow(header)
                writer.writerow(data)

    # Send email after updating the CSV
    send_email()

# Run the job search every 24 hours
if __name__ == "__main__":
    while True:
        find_jobs()
        waiting_time = 24
        print(f'Waiting for {waiting_time} hours...')
        time.sleep(waiting_time * 3600)

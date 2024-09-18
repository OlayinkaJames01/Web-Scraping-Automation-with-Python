import smtplib
import time
import schedule

def send_mail():
    try:
        # Set up the email server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('your_email@gmail.com', 'your_app_password')  # Use an app password for security
        
        # Email content
        subject = "Python Job Posting!"
        body = ("James, your dream Python job has been posted. "
                "Don't miss out! You can check your spreadsheet or proceed with the link here: "
                "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=")

        msg = f"Subject: {subject}\n\n{body}"

        # Send the email
        server.sendmail('your_email@gmail.com', 'recipient_email@gmail.com', msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Schedule the email to be sent every 24 hours
schedule.every(24).hours.do(send_mail)

# Keep the script running
if __name__ == "__main__":
    print("Scheduler started. Waiting to send emails every 24 hours...")
    while True:
        schedule.run_pending()
        time.sleep(1)


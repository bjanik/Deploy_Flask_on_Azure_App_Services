import os
import ssl

from email.mime.text import MIMEText
from dotenv import load_dotenv
from smtplib import SMTP_SSL

load_dotenv()
EMAIL_SRC = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

def send_email(email_rcv, anecdotes):
    msg = MIMEText("'Did you know' anecdotes from wikipedia has new entries", 'html')
    msg['Subject'] = 'Wikipedia anecdotes'
    msg['From'] = EMAIL_SRC
    msg['To'] = email_rcv

    message = '\n'.join(anecdotes)

    s = SMTP_SSL(host='smtp.gmail.com', port=465)
    s.login(user=EMAIL_SRC, password=PASSWORD)
    s.sendmail(EMAIL_SRC, email_rcv, message.encode())
    s.quit()
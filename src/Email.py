import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import os

def create_message(body):
    msg = MIMEText(body)
    msg['Subject'] = "YouTube Proxy New Register Request"
    msg['From'] = os.environ.get("VERIFICATION_EMAIL")
    msg['To'] = os.environ.get("VERIFICATION_EMAIL")
    msg['Date'] = formatdate()
    return msg


def send_mail(body_msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(os.environ.get("VERIFICATION_EMAIL"), os.environ.get("PASSWORDFOREMAIL"))
    smtpobj.sendmail(os.environ.get("VERIFICATION_EMAIL"), os.environ.get("VERIFICATION_EMAIL"), body_msg.as_string())
    smtpobj.close()
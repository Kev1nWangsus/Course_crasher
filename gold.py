# Author : Shuo Wang (Kevin)

# This program helps detect any available space for your target course
#  iff waitlist is not enabled and you want to change schedule due to 
#  time conflict or other personal reasons

import smtplib
import argparse
import requests
import json
import sqlite3
import time
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr 


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text

# Be sure to replace below with your email address and security password
sender = "" 
password = ""

# add target recipients here
recipients = []
smtp_server = "smtp.gmail.com"

course = {'q':'20202', 'id':'PHYS2'} 
# replace with your preferred quarter and course title
enrollcode = "38513"
# replace with your preferred course enrollcode

timeCount = 0

while(not time.sleep(60)):
    msg = MIMEMultipart()
    msg['Subject'] = "New Update!"
    msg['From'] = "GOLD Crasher"
    msg['To'] = ", ".join(recipients)    

    response = requests.get('https://web.gogaucho.app/api/sche/getClassByID', params = course)
    print("Updated!")

    jdata = json.loads(jprint(response.json()))

    server = smtplib.SMTP(host=smtp_server, port=587)
    server.starttls()
    server.login(sender, password)

    count = 0
    msg.attach(MIMEText("Course Title: %s \n" % course['id'], 'plain'))
    for i in jdata["classSections"]:
        space = i["maxEnroll"] - i["enrolledTotal"]
        if space:
            count += 1
            if i["enrollCode"] == enrollcode:
                if not timeCount:
                    print("Found!")
                    msg.attach(MIMEText("The course with enrollment code %s has %d available space right now!" % (enrollcode, space), 'plain'))
                    server.sendmail(sender, recipients, msg.as_string())
                    server.quit()
                    timeCount = 10
                else:
                    timeCount -= 1
    if not count:
        if not timeCount:
            msg.attach(MIMEText("All sections are full! \n Log in to see if waitlist is enabled. \n", 'plain'))
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            timeCount = 10
        else:
            timeCount -= 1

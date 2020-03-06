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

import autolog

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text


sender = ""
password = ""
# replace with your email and your security password

recipients = [""]
# add your preferred email to receive notification
smtp_server = "smtp.gmail.com"

course = {'q': '20202', 'id': ''}
# replace with your preferred quarter and course title
enrollcode = [""]
# replace with all your preferred course enrollcodes

timeCount = 0
addflag = 1

while(not time.sleep(60)):
    msg = MIMEMultipart()
    msg['Subject'] = "New Update!"
    msg['From'] = "GOLD Otto Crasher"
    msg['To'] = ", ".join(recipients)

    response = requests.get(
        'https://web.gogaucho.app/api/sche/getClassByID', params=course)
    print("Updated!")

    jdata = json.loads(jprint(response.json()))

    server = smtplib.SMTP(host=smtp_server, port=587)
    server.starttls()
    server.login(sender, password)

    count = 0
    msg.attach(MIMEText("Course Title: %s \n" % course['id'], 'plain'))
    for i in jdata["classSections"]:
        space = i["maxEnroll"] - i["enrolledTotal"]
        if space > 0:
            count += 1
            if i["enrollCode"] in enrollcode:
                if not timeCount and addflag:
                    print("Found!")
                    msg.attach(MIMEText("The course with enrollment code %s has %d available space right now!" % (
                        enrollcode, space), 'plain'))
                    autolog.autoAdd(i["enrollCode"])
                    msg.attach(MIMEText("Added!", 'plain'))
                    server.sendmail(sender, recipients, msg.as_string())
                    server.quit()
                    addflag -= 1
                   
    if not count:
        if not timeCount:
            msg.attach(MIMEText(
                "All sections are full! \n Log in to see if waitlist is enabled. \n", 'plain'))
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            timeCount = 10
        else:
            timeCount -= 1
    if !addflag:
        break

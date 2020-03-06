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
import autolog

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmail():
    smtp_server = "smtp.gmail.com"
    server = smtplib.SMTP(host=smtp_server, port=587)
    server.starttls()
    server.login(sender, senderpw)
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()

# Enter target quarter and course here!!!!!
currentQuarter = "20202"
targetCourse = "PHYS2"



settings = json.loads(open("settings.json",mode='r').read())

# load email notification settings
sender = settings["email"]["sender"]
senderpw = settings["email"]["senderpw"]
recipients = settings["email"]["receiver"]

# load GOLD user settings
usernameStr = settings["user"]["username"]
passwordStr = settings["user"]["password"]

# load course information
enrollCodeList = settings["quarter"][currentQuarter]["courses"][targetCourse]

web = {'q': currentQuarter, 'id': targetCourse}

sentCount = 0
addflag = 1

while(not time.sleep(60)):
    msg = MIMEMultipart()
    msg['Subject'] = "New Update!"
    msg['From'] = "GOLD otto crasher"
    msg['To'] = recipients
    msg.attach(MIMEText("Course Title: %s \n" % targetCourse, 'plain'))

    response = requests.get(
        'https://web.gogaucho.app/api/sche/getClassByID', params=web)
    print("Updated!")

    currentCourseInfo = response.json()

    courseCount = 0

    for i in currentCourseInfo["classSections"]:
        space = i["maxEnroll"] - i["enrolledTotal"]
        if space > 0:
            courseCount += 1
            if i["enrollCode"] in enrollCodeList and addflag:
                    print("Found!")
                    msg.attach(MIMEText("The course with enrollment code %s has %d available space right now!\n" % (
                        i["enrollCode"], space), 'plain'))
                    autolog.autoAdd(i["enrollCode"], usernameStr, passwordStr)
                    msg.attach(MIMEText("Added!", 'plain'))
                    sendEmail()
                    addflag -= 1
                   
    if not courseCount:
        if not sentCount:
            sentCount = 10
            msg.attach(MIMEText(
                "All sections are full! \n Log in to see if waitlist is enabled. \n", 'plain'))
            sendEmail()
            
        sentCount -= 1

    if not addflag:
        break

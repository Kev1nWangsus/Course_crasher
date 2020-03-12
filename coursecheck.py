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
targetCourse = "CMPSC24"

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

    seats = [17, 16]
    i = currentCourseInfo["classSections"][0]
    newspace = i["maxEnroll"] - i["enrolledTotal"]
    if newspace != seats[-1]:
        print("-1")
        msg.attach(MIMEText("The course with enrollment code %s has only %d spaces now :(\n" % (
            i["enrollCode"], newspace), 'plain'))
        sendEmail()
        seats.append(newspace)
        seats.pop(0)
        

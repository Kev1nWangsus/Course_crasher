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

import smtplib
import argparse

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = "1875689740ws@gmail.com"
password = "kmcechrwxrgqlcan"
to_addr = "shuo_wang@ucsb.edu"
smtp_server = "smtp.gmail.com"

msg = MIMEMultipart()
msg['From'] = _format_addr("GOLD %s" % from_addr)
msg['To'] = _format_addr("Receiver %s" % to_addr)
msg['Subject'] = Header("GOLD Enrollment", 'utf-8').encode()

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text

course = {'q':'20202', 'id':'PHYS2'}
enrollcode = "38513"

while(not time.sleep(5)):
    response = requests.get('https://web.gogaucho.app/api/sche/getClassByID', params = course)
    print("Updated!")

    jdata = json.loads(jprint(response.json()))

    count = 0
    msg.attach(MIMEText("Course Title: %s \n" % course['id'], 'plain'))
    for i in jdata["classSections"]:
        space = i["maxEnroll"] - i["enrolledTotal"]
        if space and i["enrollCode"] == enrollcode:
            print("The course you are looking for has %d spots available." % (space))
            msg.attach(MIMEText("! The course with enrollment code %s you are looking has %d available space !" % (enrollcode, space), 'plain'))
            server = smtplib.SMTP(host=smtp_server, port=587)
            server.starttls()
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
    #     elif space > 0:
    #         print("Course with enrollcode %s has %d spot(s) available." % (i["enrollCode"], space))
    #         msg.attach(MIMEText("Course with enrollcode %s has %d spot(s) available.\n" % (i["enrollCode"], space), 'plain'))
    #         count += 1
    # if count == 0:
    #     print("Sorry, no section or course is availble right now :(")
    #     msg.attach(MIMEText("Sorry, no section or course is availble right now :(", 'plain'))


# if __name__ == '__main__':
#     main()




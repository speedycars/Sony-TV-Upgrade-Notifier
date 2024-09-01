# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from lxml import etree
import os
import datetime
import time
import re
import smtplib
import random

def requests_retry_session(
    retries=50,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

httpheaders = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

while True:

    mainurltv = 'https://www.sony.bg/electronics/support/televisions-projectors-oled-tvs-android-/xr-55a83j'
    server = smtplib.SMTP('IP', PORT)
    server.login("USERNAME", "PASSWORD")
    #SONY A83J
    mainurltv = requests_retry_session().get(mainurltv, headers=httpheaders)
    sonytvsoup = BeautifulSoup(mainurltv.text.encode('utf-8'), 'html.parser')
    #print (sonytvsoup)

    headers = ("Message-ID: <"+str(random.randint(1000000000000000000000000000,9999999999999999999999999999))+"@mailer.DOMAIN.com>\nFrom: name1 <user1@domain1.com>\nTo: name2 <user2@domain2.com>\nSubject: Sony TV Upgrade Available\nMIME-Version: 1.0\nContent-Type: text/html; charset=utf-8\nContent-Transfer-Encoding: 8bit\n")

    version_element_tv = etree.HTML (str(sonytvsoup))
    version_element_tv = version_element_tv.xpath('//span[@class="item-headline t6-light downloads"]/text()')[0].replace('Актуализация на фърмуера до v','')
    print('Version number on Sony\'s website: '+version_element_tv)
    f = open( 'PATHTOTEMPTXTFILE/latestA83.txt', 'r' )
    if (not (version_element_tv in f.read())):
        msg = ('\n\n<!DOCTYPE html><head><meta charset="UTF-8"></head><body><p style="margin-top:0in;margin-right:0in;margin-bottom:8.0pt;margin-left:0in;line-height:107%;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">New upgrade for Sony Google TV (A83J): '+version_element_tv+'\n<br>Please check your tv.\n<br></p>'+'</body></html>\n\n')
        server.sendmail("MAILFROMADDRESS", "MAILTOADDRESS", headers+msg)
        f.close()
        f = open('PATHTOTEMPTXTFILE/latestA83.txt', 'w')
        print ('Saved in the temp file: '+str(version_element_tv))
        f.seek(0,2)
        print(version_element_tv)
        f.write(version_element_tv)
        f.close()
    else: print('No new version was detected for the TV. Nothing written in the temp file.\n')
    f.close()

    server.quit
    print('Cycle done! '+str(datetime.datetime.now())[0:-7]+'\n\n\n')
    for i in range(3600):
        time.sleep(1)

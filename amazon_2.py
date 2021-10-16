from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
import time
import mysql.connector

proxyList = []
workingProxy = []
badProxy = []
headers = { 'User-Agent': '(iPhone; iOS 7.0.4; Scale/2.00)'}
URLproxy = 'https://free-proxy-list.net'
mydb = mysql.connector.connect(host="localhost",
    user="zazir",
    password="0P9o8i7u@",
    #port="8819",
    database="parsamaz"
)
if(mydb):
   cursor = mydb.cursor(buffered=True)
cursor.execute('INSERT INTO info_data (field_name, field_value) VALUES ("title","%s")'%("AZAZA"))
mydb.commit()
# while len(workingProxy)<5:
#     page = requests.get(URLproxy)


#     soup = BeautifulSoup(page.content, 'html.parser')
#     tableStriped = soup.find(class_='table-striped')

#     if(tableStriped):
#         for z in tableStriped.find('tbody').find_all('tr'):
#             tds = z.find_all('td')
#             ip = tds[0].text
#             port = tds[1].text
#             https = tds[6].text == "yes"
#             #if(https):
#             proxyList.append(ip+":"+port)
#             # print(proxyList,ip)
#     if(proxyList):
#         for z in proxyList:
#             try:
#                 proxy = {"http": "http://"+z}
#                 print(proxy)
#                 r = requests.get('https://www.bing.com/', proxies=proxies, headers=headers, timeout=5)
#                 workingProxy.append(proxyList(proxy_index))
#             except:
#                 print("err")
#         #print(tds[0].text+":"=tds[1].text)
#     print(workingProxy)
#     time.sleep(5)
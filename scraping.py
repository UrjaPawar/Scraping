# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 23:00:17 2017

@author: Urja
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from commonregex import CommonRegex
import urllib,re


print("Enter the search term")
query=input()
page = requests.get("https://search.yahoo.com/search?ei=utf-8&fr=tightropetb&type=11745&p="+query)
#page = requests.get("https://www.google.dz/search?q="+query)
soup = BeautifulSoup(page.content, 'lxml')

urls = []
titles=[]
headers = soup.findAll('h3', {"class": "title"})
titles=[]
for header in headers:
    if not header.a:
        continue
    u = header.a.get('href')
    t=header.a.get_text()
    urls.append(u)
    titles.append(t)


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
ph=[]
emails=[]
addr=[]
possible_page=["","contact.htm","#contact","contact-us.htm","contact_us.htm"]


for url in urls:
    #booleans to check whether the phone,email and addr details have been assigned to a URL or not
    pb=False
    eb=False
    ab=False
    for page in possible_page:
        new_url=url+page
        print(new_url)
        try:
            req = urllib.request.Request(new_url,headers=hdr)
            f = urllib.request.urlopen(req)
            s = f.read().decode('utf-8')
            p=(re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})",s))
            e=(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s))
            # address is meant for pure US websites and is not at all 100% accurate
            a=(re.findall(r"\w[A-Za-z ]+, [A-Z]{2}",s))
            p=list(set(p))
            e=list(set(e))
            a=list(set(a))
            if (len(p)!=0 and pb==False):#phone numbers are very common
                temp=[]
                for no in p:
                    if(len(str(no))==10 or len(str(no))==11):
                        temp.append(no)
                if(len(temp)!=0):
                    ph.append(temp[0])
                else:
                    ph.append(p[0])
                pb=True
            if(len(e)!=0 and eb==False):
                emails.append(e)
                eb=True
            if(len(a)!=0 and ab==False):
                addr.append(a[0])
                ab=True   
           
        except(urllib.request.HTTPError):
            #ignore
            print("No such page")
        
    if(pb==False):
        ph.append([])
    if(eb==False):
        emails.append([])
    if(ab==False):
        addr.append([])
df=pd.DataFrame({'Title':titles,'URL':urls,'Phone':ph,'Emails':emails,'Address':addr})
df_reorder = df[['Title', 'URL', 'Phone', 'Emails', 'Address']] # rearrange column 
df_reorder.to_csv('results.csv', index=False)
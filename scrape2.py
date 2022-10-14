# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:48:54 2022

@author: marvi
"""

#tutorial from:
#https://realpython.com/python-web-scraping-practical-introduction/

# =============================================================================
# from urllib.request import urlopen
# 
# url = "https://sailboatdata.com/sailboat/11-meter"
# 
# page = urlopen(url)
# #page
# 
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# 
# #print (html)
# =============================================================================



from bs4 import BeautifulSoup
from urllib.request import urlopen
from sqlalchemy import text
from cleantext import clean
import requests, sqlalchemy
import re
import pandas as pd


def db_connect():
    #laptop-2gevqifa
    engine = sqlalchemy.create_engine('mysql+mysqldb://Horst:Hurensohn69!@laptop-2gevqifa:3306')
    return engine


def mr_clean(text):
    
    return clean(text=text,
            fix_unicode=True,
            to_ascii=True,
            lower=True,
            no_line_breaks=False,
            no_urls=False,
            no_emails=False,
            no_phone_numbers=False,
            no_numbers=False,
            no_digits=False,
            no_currency_symbols=False,
            no_punct=False,
            replace_with_punct="",
            replace_with_url="This is a URL",
            replace_with_email="Email",
            replace_with_phone_number="",
            replace_with_number="123",
            replace_with_digit="0",
            replace_with_currency_symbol="$",
            lang="en"
            )
    


def get_boats():
    sitelist = []
    r = requests.get("https://sailboatdata.com/sitemap.xml")
    xml = r.text
    
    soup = BeautifulSoup(xml, features="lxml")
    locs = soup.find_all("loc")

    engine = db_connect()
    with engine.connect() as connection: 
        #Run my query 
        result = connection.execute(text("select user from mysql.user"))
        
        print (result)
        
    for loc in locs:
       url = loc.text
       if "/sailboat/" in url:
           sitelist.append(loc.text)
   
    return sitelist
    
boats = get_boats()
# =============================================================================
# print(xml)
# print(len(xml))
# =============================================================================
boats.pop(0)
#remove first cause its a bad link
for boat in boats:
   print(boat)
   url = boat
   page = urlopen(url)
   html = page.read().decode("utf-8")
   soup = BeautifulSoup(html, "html.parser")
   sitetxt = soup.get_text()
   squeaky = mr_clean(sitetxt)

   print(squeaky)
#   with open('cleaned.txt', 'w') as f:
 #      print(sitetxt, file=f)
   
   break





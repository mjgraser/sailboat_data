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


def strip_whitespace(text):
    
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

   url = boat
   print(url)
   page = urlopen(url)
   raw_html = page.read().decode("utf-8")
   parsed_html = BeautifulSoup(raw_html, "html.parser")
   dirty_text = parsed_html.get_text()
   
   no_whitespace_text = strip_whitespace(dirty_text)
   
   #find the character number where this is (everything before it isn't uselful)
   start_delimiter =("compare\nback\n")
   start_index = no_whitespace_text.find(start_delimiter)
   #same as above
   end_delimiter =("\nsailboat links\n")
   end_index = no_whitespace_text.find(end_delimiter)
   
   #remove all the junk before compare\nback and after sailboat links
   no_whitespace_text = no_whitespace_text[start_index+len(start_delimiter):end_index]

   ## get all the headers for a page
   #use regex to define headers 
   pattern = r"[a-zA-Z./ ()#]{1,}:\n"
   headers = re.findall(pattern , no_whitespace_text)
   
   #Split on new lines - creates a list based on the delimiter character
   results = no_whitespace_text.split('\n')
   

   
   for header in headers:
       #Remove newline character since our string doesn't have it 
       header = header.strip('\n')
       #get the line number of the header
       header_line = results.index(header)
       #data is on the next line
       data = results[header_line + 1]
       
   



    # loop headers through no_whitespace_text

#   with open('cleaned.txt', 'w') as f:
#      print(sitetxt, file=f)
   break
#test




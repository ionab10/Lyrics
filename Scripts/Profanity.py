'''
Script to scrape profane words from https://www.noswearing.com/dictionary
'''

import requests
from bs4 import BeautifulSoup

profane=[]

for char in list('abcdefghijklmnopqrstuvwxyz'):
    response=requests.get("https://www.noswearing.com/dictionary/{}".format(char))
    html=BeautifulSoup(response.text)
    [h.extract() for h in html.find_all(attrs={'name':'top'})]
    profane=profane+[a.get('name') for a in html.find_all('a', href=None)]
    
profane

with open('../Data/profanity.txt','w') as f:
    for word in profane:
        f.write(word+'\n')





# References:
# https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
# http://www.jw.pe/blog/post/quantifying-sufjan-stevens-with-the-genius-api-and-nltk/
# https://github.com/johnwmillr/song-lyrics-analysis

import urllib.request
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import numpy as np
import requests, json
from time import sleep, time
import re
import random
from ast import literal_eval
from threading import Thread
from queue import Queue
import json

with open('../creds.json') as f:
    creds = json.load(f)

headers = {'Authorization': 'Bearer ' + creds['Genius']}

def search(song_title,artist_name):
    response = requests.get("http://api.genius.com/search?q={}%20{}".format(song_title,artist_name), headers=headers)
    json = response.json()
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            return hit["result"]["api_path"]
    return None

def get_release_date(song_api_path):
    song_url = "http://api.genius.com" + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    return json['response']['song']['release_date']
    
def get_tracking_targeting_data(html):
    data=html.find_all('script', string=re.compile("var (TRACKING_DATA|targeting_list)"))
    data=[re.search('(?<=var TRACKING_DATA = )[^;]+',data[0].get_text()), re.search('(?<=var targeting_list = )[^;]+',data[1].get_text())]
    data=[x.group(0).replace('true','True').replace('false','False').replace('null','None') for x in data]
    data=[literal_eval(x) for x in data]
    data[1]=dict([(x['name'],x['values'][0]) if x['values'] else (x['name'],None) for x in data[1]])
    data={**data[0],**data[1]}
    return data
    
def get_song_information(song_title,artist_name):
    song_api_path=search(song_title,artist_name)
    
    if song_api_path:
        path = "https://genius.com{}".format(song_api_path)
            
        try:
            page = requests.get(url=path)
                
            html = BeautifulSoup(page.text, "html.parser")
        
            data=get_tracking_targeting_data(html)
            
            data['release_date']=get_release_date(song_api_path)

            return data

        except:
            return None
            
    return None

def get_data_for_songs(df,outfile):
    start=time()
    for i,row in df.iterrows():
        data=get_song_information(row['song'],row['artist'])
        if data:
            for k in ['Lyrics Language',
                      'Tag',
                      'release_date',
                      'Primary Album'
                      ]:
                if data[k]:
                    df.at[i,k] = data[k]

        if i%500==0:
            print('{} {}'.format(i,outfile))
            
    df.to_csv(outfile,sep=',',encoding='utf-8')
    
    print('{} songs in {} seconds'.format(len(df),time()-start))

if __name__ == '__main__':
    
    songs_df=pd.read_csv('../Data/songdata.csv', low_memory=False)
    #songs_df=songs_df.iloc[:]
    arg_list=np.array_split(songs_df,10)
    
    threads=[]

    print('Starting...')
    for i,a in enumerate(arg_list):
        t=Thread(target=get_data_for_songs, args=(pd.DataFrame(a), "../Data/songs{}.csv".format(i)))
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
        
    #merge files
    songs_new=pd.DataFrame()
    for i in range(len(arg_list)):
        songs_new=songs_new.append(pd.read_csv("../Data/songs{}.csv".format(i), sep=',', encoding='utf-8'))
    print(songs_new.columns)
    songs_new.to_csv('../Data/songdata.csv', sep=',', encoding='utf-8')


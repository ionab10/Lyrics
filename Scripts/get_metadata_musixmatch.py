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
from musixmatch import Musixmatch

with open('../creds.json') as f:
    creds = json.load(f)
    
musixmatch = Musixmatch(creds['musiXmatch'])

def get_song_information(song_title,artist_name):
    song=musixmatch.matcher_track_get(song_title, artist_name)
    try:
        song=song['message']['body']['track']
        song['genre']=song['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
    except:
        song['genre']=None
    return song
        
def get_data_for_songs(df,outfile):
    start=time()
    for i,row in df.iterrows():
        data=get_song_information(row['song'],row['artist'])
        if data:
            for k in ['instrumental',
                      'track_length',
                      'track_rating',
                      'genre',
                      'explicit',
                      'first_release_date',
                      'album_name',
                      'track_id'
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


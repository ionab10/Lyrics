# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import time
import numpy as np
from threading import Thread

def get_metadata(artist,song):  
    response=requests.get('https://www.google.ca/search?q={}+{}'.format(artist,song))
    html=BeautifulSoup(response.content, 'lxml')
    temp=html.find_all('span', class_= ['cC4Myd','A1t5ne'])
    return [t.text for t in temp]

def get_data_for_songs(df,outfile):
    print('starting...')
    start=time()
    for i,row in df.iterrows():
        data=get_metadata(row['artist'].replace(' ','+'),row['song'].replace(' ','+'))
        while data:
            df.set_value(i,data.pop(0), data.pop(0))
            
    df.to_csv(outfile,sep=',',encoding='utf-8')
    
    print('{} songs in {} seconds'.format(len(df),time()-start))

if __name__ == '__main__':
    
    songs_df=pd.read_csv('songdata.csv')

    songs_df=songs_df.head(100)
    arg_list=np.array_split(songs_df,4)
    
    threads=[]

    for i,a in enumerate(arg_list):
        t=Thread(target=get_data_for_songs, args=(pd.DataFrame(a), "songs{}.csv".format(i)))
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
        
    #merge files
    songs_new=pd.DataFrame()
    for i in range(len(arg_list)):
        songs_new=songs_new.append(pd.read_csv("./songs{}.csv".format(i), sep=',', encoding='utf-8'))
    songs_new.reset_index(inplace=True, drop=True)
    songs_new.to_csv('songdata_v2.csv', sep=',', encoding='utf-8')


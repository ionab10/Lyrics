import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

song_df=pd.read_csv("./Data/song_vecs100.csv",sep=',',encoding='utf-8')
song_df.set_index('index',inplace=True)
print(len(song_df))
song_df.head()

topics=['LOVE',
 'HAPPINESS',
 'CHRISTMAS',
 'SADNESS',
 'ANGER',
 'REMINISCING',
 'POWER',
 'MONEY',
 'RELIGION',
 'DRUGS',
 'INSPIRATION']

data_samples=[]

for topic in topics:
    sim=model.docvecs.most_similar([model.wv[topic.lower()]], topn=100)
    doc_list=[song_df.loc[int(s[0])].lyrics for s in sim]
    all_lyrics='\n'.join(doc_list)
    data_samples.append(all_lyrics)
    
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(data_samples)
tfidf = pd.DataFrame(tfidf.toarray(), columns=tfidf_vectorizer.get_feature_names())
tfidf['Topic']=topics
tfidf.set_index('Topic', inplace=True)
tfidf

to_write=[]
for i,row in tfidf.iterrows():
    top_words=sorted(row.iteritems(), key= lambda x: x[1], reverse=True)
    to_write.append(i+'\t'+' '.join([w[0] for w in top_words[:100]]))
    print(i+'\t'+' '.join([w[0] for w in top_words[:10]]))

with open('./Data/topics-master.txt', 'w') as f:
    f.write('\n'.join(to_write))

print('Done')

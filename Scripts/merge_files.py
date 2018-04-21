import pandas as pd


filenames=[
    '../Data/songdata_v2_5_3.csv',
    ]

master=pd.read_csv('../Data/songdata_master.csv', sep=',', encoding='utf-8', low_memory=False)

for filename in filenames:
    temp=pd.read_csv(filename, sep=',', encoding='utf-8')
    master=master.append(temp)

master.reset_index(inplace=True, drop=True)
master.to_csv('../Data/songdata_master.csv', sep=',', encoding='utf-8')

print('merge successful')

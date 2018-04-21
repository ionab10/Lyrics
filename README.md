# Lyrics
A song has two main components: the music and the lyrics (sometimes lack thereof). The purpose of this project is to identify patterns and trends in song lyrics. We also look to classify songs by genre or by topic using their lyrics. From this analysis, we hope to gain insight into the music industry and pop-culture which could influence song-writing and playlist creation. 

## Code
The analysis is done in a series of iPython notebooks ('Notebooks' folder), with the occasional use of Python scripts (included in the 'Scripts' folder).
### Scripts
* get_metadata_genius.py: (Requires free API; no call limit)
* get_metadata_musixmatch.py: Scrape metadata from MusixMatch (Requires API; free API has 2000 daily call limit) 
* get_topic_vectors.py: Estimate topic vectors from training dataset (csv)
* merge_files.py: Util script for merging csv's
* Profanity.py: Scrape profanity dictionary from https://www.noswearing.com/dictionary

## Data
Data is stored in the 'Data' folder. However, not all data is uploaded to Git as the files are too large.

## Figures
Matplotlib charts are plotted inline and sometimes also saved in the 'Figures' folder. The latex document refers to this folder.

## Dependencies
* Numpy
* SciPy
* Pandas
* Matplotlib
* Plotly
* Gensim
* iPyWidgets
* Jupyter Dashboards

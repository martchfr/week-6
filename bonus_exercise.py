from apputil import *
import numpy as np
from joblib import Parallel, delayed
import psutil
import os

# Get Artist List from Text File
with open("artists.txt", "r") as file:
    artist_list = file.read().splitlines()

# Performance Tuning
thread_count  = os.cpu_count() # Determine number of jobs based on my CPU (Dynamic)
artist_chunks = np.array_split(artist_list, thread_count) # Split artist list accordingly

# Initalizae class and call get_artists() with multiple jobs
genius = Genius()
artist_dfs = Parallel(n_jobs=16, backend="threading", verbose=1)(
    delayed(genius.get_artists)(list(chunk)) for chunk in artist_chunks
)

df_artist = pd.concat(artist_dfs, ignore_index=True)

# Generate csv file
df_artist.to_csv('artists_info.csv')


from tag_mining import (
    search_tag,
    mine_tag,
    get_counts,
    data_frame,
)
from datetime import datetime
import time
import pandas as pd
import numpy as np

class Miner:
    def __init__(self, tag, intervals=60, sets=3):
        self.tag = tag
        self.intervals = intervals
        self.sets = sets
        self.realtime_logging("Hashtag Miner Started")
        self.df = self.start_miner()

    
    def get_time(self):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        return time
    
    def realtime_logging(self, text):
        time = self.get_time()
        with open('activity.txt', 'a') as f:
            f.write(f"{time}  -------------> {text}\n")

    def start_miner(self):
        tag_list = mine_tag(self.tag) #list
        self.realtime_logging("Hashtag Mining Completed!")

        data = {'hashtag': tag_list}
        df = pd.DataFrame(data) #DF

        for i in range(0, self.sets):
            time = self.get_time()
            counts = get_counts(tag_list) #list
            df.insert(i+1, time, counts)
            df.to_csv('hashtag.csv')
            self.realtime_logging(f"{i+1}/{self.sets} completed!")
            time.sleep(60*self.intervals)
        with open('activity.txt', 'a') as f:
            f.write("Session Finished\n")
        return df
    
def analyze(filename):
    df = pd.read_csv(filename)
    data = {}
    for i in range(1, len(df.columns)):
        data[f'inc-rate{i}'] = df[df.columns.values[i+1]] / df[df.columns.values[i]]
    preview = pd.DataFrame(data, index=df["hashtag"])
    rank_df = preview.apply(np.argsort, axis=1)
    ranked_cols = df.columns.to_series()[rank_df.values[:,::-1][:,:2]]
    data = {
        'latests': df[df.columns[-1]],
        'hot-time': ranked_cols[0], #highest increase interval
        '2nd hot-time': ranked_cols[1], #2nd highest
        'mean': preview.mean(axis=1) #mean of every difference
    }
    df_analysis = pd.DataFrame(data, index=df['hashtag'])
    df_analysis.to_csv("analysis.csv")


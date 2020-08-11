from tag_mining import mine_tag, get_counts
from datetime import datetime
import time
import pandas as pd
import numpy as np

class Miner:
    def __init__(self, tag, custom, intervals=60, sets=3):
        self.tag = tag
        self.custom = custom
        self.intervals = intervals
        self.sets = sets
        self.activity_log("Miner Activated",3)

    def activity_log(self, text: str, datetype: int):
        now = datetime.now()
        if datetype == 1:
            time = now.strftime("%d/%m/%Y")
        elif datetype == 2:
            time = now.strftime("%H:%M:%S")
        else:
            time = now.strftime("%d/%m/%Y, %H:%M:%S")
        with open('activity.txt', 'a') as f:
            f.write(f"{time} --------> {text}\n")

    def start_miner(self):
        mine_tag(self.tag, self.custom)
        for attempt in range(self.sets):
            get_counts(f"{self.tag}.csv")
            time.sleep(60*self.intervals)
            self.activity_log(f"{attempt+1}/{self.sets} sets completed",2)
        self.activity_log("Mining Completed!", 3)

    def analyze(self, filename):
        df = pd.read_csv(filename, index_col=0)
        df.set_index('hashtags', inplace=True)
        df = df.transpose()
        
        Data = {}


    
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
        df_analysis.to_csv(f"{filename}-analysis.csv")


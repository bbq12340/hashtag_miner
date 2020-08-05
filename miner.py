from tag_mining import (
    search_tag,
    mine_tag,
    get_counts,
    data_frame,
)
from datetime import datetime
import time
import pandas as pd

class Miner:
    def __init__(self, tag, intervals=60, sets=3):
        self.tag = tag
        self.intervals = intervals
        self.sets = sets
        self.realtime_logging("Hashtag Miner Started")
        self.start_miner()
    
    def realtime_logging(self, text):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        with open('activity.txt', 'a') as f:
            f.write(f"{time}  -------------> {text}\n")

    def start_miner(self):
        tag_list = search_tag(self.tag)
        data = mine_tag(tag_list)
        self.realtime_logging("Hashtag Mining Completed!")
        for i in range(0, self.sets):
            counts = get_counts(data["hashtag"])
            data = data_frame(data, counts)
            data.to_csv('hashtag.csv')
            self.realtime_logging(f"{i+1}/{self.sets} completed!")
            time.sleep(60*self.intervals)
        df = data.set_index('hashtag')
        now = datetime.now()
        date = now.strftime("%m/%d/%Y, %H:%M:%S")
        with open('activity.txt', 'a') as f:
            f.write(f"{date} | Session Finished\n")
        return df
    
    def analyze(self, filename):
        df = pd.read_csv(filename)
        target_data = {"hastag": list(df.index.values)}
        analysis_df = pd.DataFrame(target_data)
        for n in range(1, len(df.columns)):
            former = df.columns[n]
            latter = df.columns[n+1]
            diff = df[latter] - df[former]
            analysis_df[f'diff{n}'] = diff
        analysis_df = analysis_df.set_index("hashtag")
        analysis_df['mean'] = analysis_df.mean(axis=1)
        return analysis_df

    


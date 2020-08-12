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
        df_num = df.select_dtypes(include=[np.number])
        for i in range(1, len(df.index)):
            df_diff = df.iloc[i] - df.iloc[i-1]
            df_ir = (df_diff/df_num.iloc[i-1])*100
            Data[f"interval{i}"] = df_ir
        DF = pd.DataFrame(Data)

        HOTTEST = DF.idxmax(axis=1)
        AVERAGE = DF.mean(axis=1)
        ir_average = sum(AVERAGE)/len(AVERAGE)
        ir_deviation = [x - ir_average for x in AVERAGE]
        DF['hottest'] = HOTTEST
        DF['average'] = AVERAGE
        DF['deviation'] = ir_deviation
        DF.to_csv("analysis.csv")

        df_bool = df.select_dtypes(include='bool')
        with open('banned_hashtags.txt', 'a') as f:
            for b in df_bool.columns.values:
                f.write(f"{b}\n")
        


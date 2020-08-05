from miner import Miner
import pandas as pd

miner = Miner("맛집")

df = pd.read_csv("hashtag.csv")

tags = list(df.index.values)

time = df.columns[len(df.columns)-1]
counts = list(df[time].values)

mean = miner.analyze("hashtag.csv")

DF = pd.DataFrame({
    'hashtag': tags,
    'current posts': counts,
    'average increase': mean,
})
DF.to_csv('result.csv')


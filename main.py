from tag_mining import search_tag, mine_tag, get_counts, log_csv
from datetime import datetime

def realtime_logging(text):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    with open('activity.txt', 'a') as f:
        f.write(f"{time} {text}\n")

TAG_LIST = search_tag("맛집")
realtime_logging("searching tag...")
tags = mine_tag(TAG_LIST)
realtime_logging("mining tags...")
DF = get_counts(tags)
realtime_logging("getting counts...")
log_csv(DF)
realtime_logging("finished!")



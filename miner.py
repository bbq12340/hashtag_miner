from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pandas as pd
import numpy as np
import random
import schedule
import sys

class TagMiner:
    def __init__(self, tag, custom=None, num=30):
        self.tag = tag
        self.custom = custom
        self.num = num
        self.browser = self.open_browser()
        HASHTAGS_DF = pd.DataFrame({'hashtags': self.search_mediance()})

        while len(HASHTAGS_DF['hashtags']) < self.num:
            random_tags = random.sample(list(HASHTAGS_DF['hashtags']), 10)
            NEW_DF = self.search_tagsfinder(random_tags)
            HASHTAGS_DF = pd.concat([HASHTAGS_DF, NEW_DF], ignore_index=True)
            HASHTAGS_DF.drop_duplicates(subset=['hashtags'])
            if len(HASHTAGS_DF['hashtags']) >= self.num:
                self.browser.close()
                HASHTAGS_DF.to_csv(f'{self.tag}.csv', encoding='utf-8')
                break
        self.df = pd.read_csv(f'{self.tag}.csv', index_col=0)
        
    def open_browser(self):
        browser = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(browser, 30)
        return browser
    def search_mediance(self):
        SIMILAR_RANK = 'rank_table'
        SIMILAR_RANK_BY_ID = By.CLASS_NAME, SIMILAR_RANK
        NO_RESULT = 'nosearch_con'
        HASHTAGS = []
        self.browser.get(f"http://tag.mediance.co.kr/analytics/tag/{self.tag}")
        try:
            self.wait.until(EC.presence_of_element_located(SIMILAR_RANK_BY_ID))
            html = self.browser.execute_script('return document.documentElement.outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            similar_rank_table = soup.find('table', {'class': 'rank_table'})
            table_row = similar_rank_table.find_all('tr')
            table_row.pop(0)
            for row in table_row:
                hashtag = row.find('a').text
                HASHTAGS.append(hashtag)
            return HASHTAGS
        except (TimeoutException, NoSuchElementException):
            self.browser.find_element_by_class_name(NO_RESULT)
            HASHTAGS = []
            return HASHTAGS
    def search_tagsfinder(self, hashtags):
        CLIPBOARD = 'clipboard'
        CLIPBOARD_BY_ID = By.ID, CLIPBOARD
        HASHTAGS = []
        query_tags = ('%2C%20').join(hashtags)
        self.browser.get(f"https://www.tagsfinder.com/ko-kr/?hashtag={query_tags}&limit=30&country=kr&fs=off&fp=off&fg=off&custom={self.custom}&type=mix")
        self.wait.until(EC.presence_of_element_located(CLIPBOARD_BY_ID))
        html = self.browser.execute_script('return document.documentElement.outerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('span', {'class': 'tag'})
        for tag in tags:
            tag = tag.text[1:].split('X')[0]
            HASHTAGS.append(tag)
        hashtag_df = pd.DataFrame({'hashtags': HASHTAGS})
        return hashtag_df

    def get_counts(self):
        HASHTAG_INFO_BY_CLASS = By.CLASS_NAME, "WSpok"
        COUNTS=[]

        tag_list = list(self.df['hashtags'])
        
        for t in tag_list:
            self.browser.get(f"https://www.instagram.com/explore/tags/{t}/")
            self.wait.until(EC.presence_of_element_located(HASHTAG_INFO_BY_CLASS))
            html = self.browser.execute_script('return document.documentElement.outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            count = soup.find('span',{'class':'g47SY'})
            banned = soup.find('div',{'class': '._4Kbb_'})
            posts = soup.find_all('div', {'class': 'v1Nh3'})
            if count:
                count = count.text
                if type(count) == str:
                    count = int(count.replace(',',''))
            elif banned:
                count = False
            elif posts:
                count = len(posts)
            COUNTS.append(count)
        now = datetime.now()
        current_time = now.strftime("%H")
        self.df.insert(len(self.df.columns), current_time, COUNTS)
        self.df.to_csv(f'{self.tag}.csv', index=False)
        
    def scheduler(self, start, hours):
        schedule.every().hour.at(f"{start}:00").do(self.get_counts)
        while True:
            schedule.run_pending()
            time.sleep(60)
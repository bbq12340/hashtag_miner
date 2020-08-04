import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
import time
from datetime import datetime
import csv
import pandas as pd

INSTAGRAM_QUERY = "https://www.instagram.com/explore/tags/"
HASHTAG_INFO = By.CLASS_NAME, "WSpok"
POST_COUNT = "g47SY"
RELATED_TAGS = "LFGs8"

CHILD_TAGS = [] #used in search_tags
COUNTS = [] #used in get_counts

def open_browser(q):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(INSTAGRAM_QUERY + q)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(HASHTAG_INFO))
    return driver

def data_frame(data, counts):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    df = pd.DataFrame(data, index=None)
    df[f"{time}"] = counts
    return df

def get_counts(tags):
    for t in tags:
        browser = open_browser(t)
        while True:
            try:
                post_count = browser.find_element_by_class_name(POST_COUNT).get_attribute("innerText")
                browser.close()
            except TimeoutException:
                continue
            break
        COUNTS.append(post_count)
    return COUNTS

def mine_tag(tag_list):
    TAGS = []
    TAGS.extend(tag_list)
    while len(TAGS) < 100:
        for t in range(0,100):
            while True:
                try:
                    tag_list = search_tag(TAGS[t])
                    TAGS.extend(tag_list)
                    TAGS = list(OrderedDict.fromkeys(TAGS))
                except TimeoutException:
                    continue
                break       
            if len(TAGS) >= 100:
                break
    data = {"hashtag": TAGS}
    return data


def search_tag(tag):
    browser = open_browser(tag)
    rel_tags = browser.find_elements_by_class_name(RELATED_TAGS)

    for tag in rel_tags:
        tag = tag.get_attribute('innerText').strip('#')
        CHILD_TAGS.append(tag)
    browser.close()
    return CHILD_TAGS

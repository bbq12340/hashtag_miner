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

def get_counts(tag_list):
    COUNT = []
    for t in tag_list:
        browser = open_browser(t)
        while True:
            try:
                post_count = browser.find_element_by_class_name(POST_COUNT).get_attribute("innerText")
                browser.close()
            except TimeoutException:
                continue
            break
        COUNT.append(post_count)
    return COUNT

def mine_tag(tag):
    TAGS = []
    TAGS.append(tag)
    print(len(TAGS))
    while len(TAGS) < 100:
        for t in range(0,100):
            while True:
                try:
                    print(t)
                    related_tag_list = search_tag(TAGS[t])
                    TAGS.extend(related_tag_list)
                    TAGS = list(OrderedDict.fromkeys(TAGS))
                    print(related_tag_list)
                    print(len(TAGS))
                except TimeoutException:
                    continue
                break       
            if len(TAGS) >= 100:
                break
    return TAGS

def search_tag(tag):
    REL_TAGS = []
    browser = open_browser(tag)
    rel_tags = browser.find_elements_by_class_name(RELATED_TAGS)

    for tag in rel_tags:
        tag = tag.get_attribute('innerText').strip('#')
        REL_TAGS.append(tag)
    browser.close()
    return REL_TAGS
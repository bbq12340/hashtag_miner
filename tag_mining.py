from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import csv

INSTAGRAM_QUERY = "https://www.instagram.com/explore/tags/"
HASHTAG_INFO = By.CLASS_NAME, "WSpok"
POST_COUNT = "g47SY"
RELATED_TAGS = "LFGs8"

CHILD_TAGS = []
ULTIMATE_TAGS = []

def log_csv(file_name, row_dict):
    field_names = ['timestamp', 'tag-name', 'posts']
    with open(file_name, 'w') as csvfile:
        csv_writer = csv.writer(file_name, delimiter=',', fieldnames=field_names)

def mine_tag(tag_list):
    return tag_list


def search_tag(tag):
    now = datetime.now()
    print("start mining!")
    query_tag = INSTAGRAM_QUERY + tag
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(query_tag)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located(HASHTAG_INFO))
    post_count = browser.find_element_by_class_name(POST_COUNT).get_attribute("innerText")
    rel_tags = browser.find_elements_by_class_name(RELATED_TAGS)

    TAG = {
        "timestamp": now,
        "tag-name": tag,
        "posts": post_count
    }

    ULTIMATE_TAGS.append(TAG)

    for tag in rel_tags:
        tag = tag.get_attribute('innerText').strip('#')
        CHILD_TAGS.append(tag)
    return CHILD_TAGS
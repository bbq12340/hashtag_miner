from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from collections import OrderedDict
import time
from datetime import datetime
import pandas as pd

HASHTAG_INFO = By.CLASS_NAME, "WSpok"
POST_COUNT = "g47SY"
RELATED_TAGS = "LFGs8"
rel_tags = '//*[@id="ajax"]/div/div/div[1]'
rel_tags_by = By.XPATH, rel_tags

def instagram_refresh(browser):
    for attempt in range(0, 10):
        try:
            print("trying"+attempt)
            browser.sleep(3)
            browser.refresh()
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_element_located(HASHTAG_INFO))
            post_count = browser.find_element_by_class_name(POST_COUNT).get_attribute("innerText")
        except TimeoutException:
            continue
    post_count = "TIMEOUT"
    return post_count


def open_browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver

def open_instagram(driver, q):
    driver.get(f"https://www.instagram.com/explore/tags/{q}/")
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located(HASHTAG_INFO))
    except TimeoutException:
        instagram_refresh(driver)
    return driver

def open_tagfinder(driver, q, custom):
    TAGS = []
    driver.get(f"https://www.tagsfinder.com/ko-kr/?hashtag={q}&limit=30&country=kr&fs=off&fp=off&fg=off&custom={custom}&type=mix")    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(rel_tags_by))
    rel = driver.find_element_by_xpath(rel_tags)
    li = rel.find_elements_by_tag_name("span")
    for t in li:
        t = t.get_attribute('innerText').strip('#').strip('\nX')
        TAGS.append(t)  
    return TAGS

def mine_tag(parent_tag: str, custom=""):
    HASHTAGS = []
    HASHTAGS.append(parent_tag)
    browser = open_browser()
    while len(HASHTAGS) < 100:
        for t in range(0,100):
            while True:
                try:
                    related_tag_list = open_tagfinder(browser, HASHTAGS[t], custom)
                    HASHTAGS.extend(related_tag_list)
                    HASHTAGS = list(OrderedDict.fromkeys(HASHTAGS))
                except TimeoutException:
                    continue
                break       
            if len(HASHTAGS) >= 100:
                break
    data = {'hashtags': HASHTAGS}
    df = pd.DataFrame(data)
    df.to_csv(f"{parent_tag}.csv")
    return df

def get_counts(filename):
    COUNT = []
    df = pd.read_csv(filename, index_col=0)
    tag_list = list(df['hashtags']) 
    browser = open_browser()
    #count for each hashtags
    for t in tag_list:
        print(tag_list.index(t), t)
        browser = open_instagram(browser, t)
        try:
            post_count = browser.find_element_by_class_name(POST_COUNT).get_attribute("innerText")
        except TimeoutException:
            instagram_refresh(browser)
        except NoSuchElementException:
            try:
                banned = browser.find_element_by_class_name("_4Kbb_")
                post_count = "banned"
            except NoSuchElementException:
                posts = browser.find_elements_by_class_name("v1Nh3")
                post_count = len(posts)
        COUNT.append(post_count)
    #clean count-list
    CLEANED_VALUE = []
    for elem in COUNT:
        if type(elem) == str:
            try:
                value = int(elem.replace(",",""))
                CLEANED_VALUE.append(value)
            except ValueError:
                value = elem
                CLEANED_VALUE.append(value)
        else:
            CLEANED_VALUE.append(elem)
    COUNT = CLEANED_VALUE

    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    df.insert(len(df.columns), time, COUNT)
    df.to_csv(filename, index=False)
    return COUNT
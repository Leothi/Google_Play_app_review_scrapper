import os

from loguru import logger
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from utils_text import strip_accents, preprocess_text

chrome_options = Options()
chrome_options.add_argument('headless')

NUM_REVIEWS = 10

with webdriver.Chrome(options=chrome_options) as driver:
    wait = WebDriverWait(driver, 5)

    link = "https://play.google.com/store/apps/details?id=br.com.bb.android&hl=pt&showAllReviews=true"
    all_reviews_xpath = '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div'
    name_xpath = '//*[@id = "fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/span'

    driver.get(link)

    for i in range(NUM_REVIEWS):
        logger.info(f'REVIEW #{i+1}')
        current_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{i+1}]'
        current_review = driver.find_element_by_xpath(current_xpath)

        clean_text = strip_accents(current_review.text)
        print(clean_text)

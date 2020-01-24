import os

from loguru import logger
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from utils_text import strip_accents, preprocess_text

chrome_options = Options()
chrome_options.add_argument('headless')

NUM_REVIEWS = 6

with webdriver.Chrome(options=chrome_options) as driver:
    wait = WebDriverWait(driver, 5)

    link = "https://play.google.com/store/apps/details?id=br.com.bb.android&hl=pt&showAllReviews=true"
    logger.info('[+] Scrapping Beginning')
    driver.get(link)

    for i in range(NUM_REVIEWS):
        try:
            logger.info(f'REVIEW #{i+1}')

            # Getting name
            current_name_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[1]/div[1]/span'
            current_name = driver.find_element_by_xpath(current_name_xpath)
            print(current_name.text)

            # Getting date
            current_date_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[1]/div[1]/div/span[2]'
            current_date = driver.find_element_by_xpath(current_date_xpath)
            print(current_date.text)

            # # Getting rating
            # current_rating_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/span'
            # current_rating = driver.find_element_by_xpath(current_rating_xpath)
            # print(current_rating.text)

            # Getting description
            current_button_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{i+1}]/div/div[2]/div[2]/span[1]/div/button'
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, current_button_xpath)))
            driver.find_element_by_xpath(current_button_xpath).click()

            current_description_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[2]/span[2]'
            current_description = driver.find_element_by_xpath(
                current_description_xpath)
            print(current_description.text)

        except NoSuchElementException:
            logger.warning("Element not found.")
        except ElementNotVisibleException:
            logger.warning("Element not visible")

    logger.info('[+] Scrapping DONE')

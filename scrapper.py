import pandas as pd
import random
import re

from sys import argv
from loguru import logger
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

chrome_options = Options()
chrome_options.add_argument('headless')
logger.add("scrapper.log")

excep_counter = 0
random_number_name = random.randint(0, 1000)
RE_STARS = re.compile(r'(?:Avaliado com )(\d)')


def scrapper(link: str, num_reviews: int, verbose: bool = False):
    reviews_dict = defaultdict(list)

    with webdriver.Chrome(options=chrome_options) as driver:
        wait = WebDriverWait(driver, 3)

        logger.info(f'[+] Initializing Scrapper with {num_reviews} reviews')
        try:
            driver.get(link)
        except WebDriverException:
            logger.warning("Can't get website")

        for i in range(num_reviews):
            excep_name = False
            excep_date = False
            excep_description = False
            excep_likes = False
            excep_stars = False

            # Getting name
            try:
                current_name_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[1]/div[1]/span'
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, current_name_xpath)))
                current_name = driver.find_element_by_xpath(current_name_xpath)
            except TimeoutException:
                excep_name = True
                logger.warning("Can't get name")

            # Getting stars
            try:
                stars_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{i+1}]/div/div[2]/div[1]/div[1]/div/span[1]/div/div'
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, stars_xpath)))
                current_stars = driver.find_element_by_xpath(stars_xpath)
                current_stars_text = current_stars.get_attribute('aria-label')
                current_stars_text = RE_STARS.findall(current_stars_text)[0]
            except TimeoutException:
                excep_stars = True
                logger.warning("Can't get stars")

            # Getting likes
            try:
                likes_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{i+1}]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]'
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, likes_xpath)))
                current_likes = driver.find_element_by_xpath(likes_xpath)
                current_likes_text = current_likes.text
                if not current_likes_text:
                    current_likes_text = '0'
            except TimeoutException:
                excep_likes = True
                logger.warning("Can't get likes")

            # Getting date
            try:
                current_date_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[1]/div[1]/div/span[2]'
                current_date = driver.find_element_by_xpath(current_date_xpath)
            except NoSuchElementException:
                excep_date = True
                logger.warning("Can't get date")

            # Getting description
            try:
                current_description_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[2]/span[1]'
                current_description = driver.find_element_by_xpath(
                    current_description_xpath)

                # If description is not complete, need to click "show more" button
                desc_last_word = current_description.text.split()[-1]
                if 'completa' in desc_last_word or 'review' in desc_last_word:
                    current_button_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{i+1}]/div/div[2]/div[2]/span[1]/div/button'
                    wait.until(EC.element_to_be_clickable(
                        (By.XPATH, current_button_xpath)))
                    current_button = driver.find_element_by_xpath(
                        current_button_xpath)
                    driver.execute_script(
                        "arguments[0].click();", current_button)

                    # Getting full description
                    current_description_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[2]/span[2]'
                    current_description = driver.find_element_by_xpath(
                        current_description_xpath)
            except (TimeoutException, NoSuchElementException, WebDriverException):
                excep_description = True
                logger.warning("Can't get description")

            # Scrolling down page to get more reviews
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Clicking show more button every 100 reviews to get more reviews
            if (i % 100 == 0 and i != 0):
                try:
                    show_more_button = driver.find_element_by_xpath(
                        "//*[contains(text(), 'Mostrar mais')]")
                    driver.execute_script(
                        "arguments[0].click();", show_more_button)
                except NoSuchElementException:
                    pass

            # Putting all reviews in a dict
            if not any([excep_name, excep_date, excep_description, excep_likes, excep_stars]):
                excep_counter = 0

                reviews_dict['name'].append(current_name.text)
                reviews_dict['raw_review'].append(current_description.text)
                reviews_dict['date'].append(current_date.text)
                reviews_dict['likes'].append(current_likes_text)
                reviews_dict['stars'].append(current_stars_text)

                logger.info(f'Review #{i+1} DONE')
            else:
                excep_counter += 1
                logger.warning(
                    f'Review #{i+1} NOT DONE, terminating in {3-excep_counter}')

                if excep_counter >= 3:
                    logger.success('[+] Scrapping DONE')
                    break

        return reviews_dict


def save_reviews(all_reviews: dict, output_file: str = f'scrapper_results_{random_number_name}.csv'):
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv(output_file, index=False)
        logger.success(f'[+] CSV file created. Filename: {output_file}')
    else:
        logger.warning('All_reviews dict empty')


if __name__ == "__main__":
    all_reviews = scrapper(link=argv[1], num_reviews=int(argv[2]))
    save_reviews(all_reviews)

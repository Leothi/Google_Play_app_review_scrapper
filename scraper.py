import pandas as pd

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

from utils_text import strip_accents, preprocess_text

chrome_options = Options()
chrome_options.add_argument('headless')


def scrapper(link: str, num_reviews: int, verbose: bool = False):
    reviews_dict = defaultdict(list)

    with webdriver.Chrome(options=chrome_options) as driver:
        wait = WebDriverWait(driver, 5)

        logger.info(f'[+] Initializing Scrapper with {num_reviews} reviews')
        try:
            driver.get(link)
        except WebDriverException:
            logger.warning("Can't get website")

        for i in range(num_reviews):
            try:
                # Getting name
                current_name_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[1]/div[1]/span'
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, current_name_xpath)))
                current_name = driver.find_element_by_xpath(current_name_xpath)
            except TimeoutException:
                logger.warning("Can't get name")

            try:
                # Getting date
                current_date_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[1]/div[1]/div/span[2]'
                current_date = driver.find_element_by_xpath(current_date_xpath)
            except NoSuchElementException:
                logger.warning("Can't get date")

            try:
                # Getting description
                current_description_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[2]/span[1]'
                current_description = driver.find_element_by_xpath(
                    current_description_xpath)

                # If description is not complete, need to click "show more" button
                if 'completa' in current_description.text.split()[-1] or 'review' in current_description.text.split()[-1]:
                    current_button_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{i+1}]/div/div[2]/div[2]/span[1]/div/button'
                    wait.until(EC.element_to_be_clickable(
                        (By.XPATH, current_button_xpath)))
                    current_button = driver.find_element_by_xpath(
                        current_button_xpath)
                    driver.execute_script(
                        "arguments[0].click();", current_button)

                    current_description_xpath = f'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{i+1}]/div/div[2]/div[2]/span[2]'
                    current_description = driver.find_element_by_xpath(
                        current_description_xpath)
            except (TimeoutException, NoSuchElementException):
                logger.warning("Can't get description")

            # Scrolling down pages to get more reviews
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            try:
                if verbose:
                    print(current_name.text)
                    print(current_date.text)
                    print(strip_accents(current_description.text))

                # Getting all reviews in a dict
                pre_processed_text = preprocess_text(current_name.text)
                reviews_dict['name'].append(pre_processed_text)

                reviews_dict['date'].append(current_date.text)

                pre_processed_description = preprocess_text(
                    current_description.text)
                reviews_dict['review'].append(pre_processed_description)

                logger.info(f'Review #{i+1} DONE')
            except UnboundLocalError:
                logger.warning(f'Review #{i+1} NOT DONE')

        logger.success('[+] Scrapping DONE')

        return reviews_dict


def save_reviews(all_reviews: dict, output_file: str = 'scrapper_results.csv'):
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv(output_file, ';', index=False)
    else:
        logger.warning('All_reviews dict empty')


if __name__ == "__main__":
    all_reviews = scrapper(link=argv[1], num_reviews=int(argv[2]))
    save_reviews(all_reviews)

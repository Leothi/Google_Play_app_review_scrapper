import os

from loguru import logger
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from config import *

options = webdriver.FirefoxOptions()
options.headless = True

profile = webdriver.FirefoxProfile()

# PDF Download
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager"
                       ".showWhenStarting", False)
profile.set_preference("browser.download.dir", DOWNLOADS_PATH)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       "application/pdf")

profile.set_preference("pdfjs.disabled", True)
profile.set_preference("plugin.scan.Acrobat", "99.0")
profile.set_preference("plugin.scan.plid.all", False)

profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", PROXY_HOST)
profile.set_preference("network.proxy.http_port", PROXY_PORT)
profile.set_preference("network.proxy.socks_username", PROXY_USER)
profile.set_preference("network.proxy.socks_password", PROXY_PASS)

with webdriver.Firefox(executable_path=SELENIUM_DRIVER,
                       firefox_profile=profile, options=options) as driver:
    wait = WebDriverWait(driver, 5)

    all_reviews_xpath = '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div'
    name_xpath = '//*[@id = "fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/span'

    driver.get(
        "https://play.google.com/store/apps/details?id=br.com.bb.android&hl=pt&showAllReviews=true")

    reviews = driver.find_element_by_xpath(all_reviews_xpath)
    names = reviews.find_element_by_xpath(name_xpath)

    for name in names:
        print(name.text)
    # sleep(5)
    # extracted_text = review.text

# print(extracted_text)

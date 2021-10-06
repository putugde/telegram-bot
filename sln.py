from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger('selenium')

from urllib.parse import unquote

import time
SCROLL_PAUSE_TIME = 0.3
TIMEOUT_TRESHOLD = 10

class Selenium():
    def start(self):
        logger.info('Selenium Started !')
        self.driver = webdriver.Chrome(options=chrome_options)

    def search_gimg(self, keyword, index):
        logger.info(f'Search google image with keyword {keyword} and index {index}')
        self.driver.get("https://image.google.com")
        
        search_bar = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input')
        search_bar.send_keys(keyword)

        search_button = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/button')
        search_button.click()

        timeout_counter = 0
        while True:
            try:
                chosen_image = self.driver.find_element(By.XPATH, f'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[{index}]/a[1]')
                chosen_image.click()
            except Exception:
                chosen_image = None

            if chosen_image:
                imgurl = chosen_image.get_attribute("href")
                break
            else:
                # Get scroll height
                last_height = self.driver.execute_script("return document.body.scrollHeight")

                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                # logger.error(f'NEW HEIGHT : {new_height}')
                # logger.error(f'LAST HEIGHT : {last_height}')

                if new_height == last_height:
                    timeout_counter += 1
                    if timeout_counter > TIMEOUT_TRESHOLD:
                        logger.error(f'NO PICTURE')
                        return None
                else:
                    timeout_counter = 0

        parsed_url = ((imgurl[37:]).split("&imgrefurl="))[0]
        parsed_url = unquote(parsed_url)

        return parsed_url
    
    def close(self):
        self.driver.close()
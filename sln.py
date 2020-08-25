from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger('selenium')

class Selenium():
    def start(self):
        logger.info('Selenium Started !')
        self.driver = webdriver.Chrome()

    def search_gimg(self, keyword, index):
        logger.info(f'Search google image with keyword {keyword} and index {index}')
        self.driver.get("https://image.google.com")
        search_bar = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input')
        search_bar.send_keys(keyword)

        search_button = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/button')
        search_button.click()

        chosen_image = self.driver.find_element(By.XPATH, f'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[{index}]/a[1]')
        chosen_image.click()

        imgurl = chosen_image.get_attribute("href")
        parsed_url = ((imgurl[37:]).split("&imgrefurl="))[0]
        parsed_url = (parsed_url.replace("%3A",":")).replace("%2F","/")

        return parsed_url
    
    def close(self):
        self.driver.close()
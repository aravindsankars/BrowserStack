import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Scraper:
    def __init__(self, username, access_key, article_images_path):
        self.driver_url = f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"
        self.article_images_path = article_images_path

    def create_driver(self, capabilities):
        return webdriver.Remote(command_executor=self.driver_url, desired_capabilities=capabilities)

    def fetch_articles(self, driver, base_url="https://elpais.com"):
        opinion_section_url = f"{base_url}/opinion"
        driver.get(opinion_section_url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup.find_all("article", limit=5)

    def save_image(self, image_url, file_path):
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Saved image at: {file_path}")
        else:
            print(f"Failed to download image: {image_url}")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import requests

class Scraper:
    def __init__(self, driver_path, base_url):
        self.driver = webdriver.Chrome(service=Service(driver_path))
        self.base_url = base_url

    def fetch_articles(self, section_path="opinion", limit=5):
        url = f"{self.base_url}/{section_path}"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        return soup.find_all("article", limit=limit)

    def save_image(self, image_url, save_path):
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image saved to: {save_path}")
        else:
            print(f"Failed to download image: {image_url}")

    def quit(self):
        self.driver.quit()

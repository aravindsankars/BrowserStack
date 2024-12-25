import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import os
import json
import yaml
import re
from collections import Counter
from urllib.parse import urljoin

# Load the YAML configuration
with open("secrets.yml", "r") as file:
    config = yaml.safe_load(file)

with open("browserstack.yml", "r") as file:
    bs_config = yaml.safe_load(file)


# BrowserStack credentials
BROWSERSTACK_USERNAME = config['secrets']['browserstack_username']
BROWSERSTACK_ACCESS_KEY = config['secrets']['browserstack_access_key']

# Get the parent directory of the src folder
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the path to the article_images folder
article_images = os.path.join(parent_directory, 'article_images')

# Ensure the article_images directory exists
os.makedirs(article_images, exist_ok=True)

# RapidAPI credentials
api_key = config['secrets']['rapid_api_key']
api_url = config['secrets']['rapid_api_url']


headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "rapid-translate-multi-traduction.p.rapidapi.com",
    "Content-Type": "application/json"
}

# BrowserStack capabilities for different browsers/devices
capabilities_list = bs_config['platforms']

# Function to use Rapid Translate API
def translate_text(text, source_lang='es', target_lang='en'):
    params = {
        "from": source_lang,
        "to": target_lang,
        "q": [text]
    }
    try:
        response = requests.post(api_url, json=params, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list):
                return result[0]
            else:
                return result['translated_text']
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text

# Function to tokenize and count word frequencies
def get_word_counts(text_list):
    word_counts = Counter()
    for text in text_list:
        # Tokenize the text by splitting on non-alphanumeric characters and convert to lowercase
        words = re.findall(r'\b\w+\b', text.lower())
        word_counts.update(words)
    return word_counts

def run_test(capabilities):
    # Create BrowserStack WebDriver
    driver = webdriver.Remote(
        command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=capabilities,
    )
    try:
        # Navigate to the website's Opinion section
        base_url = "https://elpais.com"
        opinion_section_url = f"{base_url}/opinion"
        driver.get(opinion_section_url)

        # Wait for articles to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))

        # Parse articles with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Locate the articles in the Opinion section
        articles = soup.find_all("article", limit=5)
        if not articles:
            print("No articles found in the Opinion section.")
            driver.quit()
            exit()

        # Create a folder to save images
        translated_titles = []
        for idx, article in enumerate(articles, start=1):
            title_tag = article.find("h2") or article.find("h3")
            title = title_tag.text.strip() if title_tag else "No title found"

            # Translate title
            translated_title = translate_text(title)
            translated_titles.append(translated_title)

            # Extract content
            content_tags = article.find_all("p")
            content = " ".join(tag.text.strip() for tag in content_tags) if content_tags else "No content found"
            print(content)

            # Attempt to find the cover image URL
            try:
                image_tag = article.find("img")
                if image_tag and "src" in image_tag.attrs:
                    image_url = urljoin(opinion_section_url, image_tag["src"])

                    # Download the image
                    image_response = requests.get(image_url, stream=True)
                    if image_response.status_code == 200:
                        # Define the file path
                        image_path = os.path.join(article_images, f"article_{idx}_cover.jpg")

                        # Save the image
                        with open(image_path, "wb") as image_file:
                            for chunk in image_response.iter_content(1024):
                                image_file.write(chunk)

                        print(f"Cover image for Article {idx} saved at: {image_path}")
                    else:
                        print(f"Failed to download cover image for Article {idx}. Status code: {image_response.status_code}")
                else:
                    print(f"No cover image found for Article {idx}.")
            except Exception as e:
                print(f"Error downloading cover image for Article {idx}: {e}")

            # Translate the content to English using Rapid Translate
            translated_content = translate_text(content)

            # Print the translated title and content
            print(f"Article {idx}: {translated_title}")
            print(translated_content)
            print("=" * 80)

    except Exception as e:
        print(f"Error in thread {capabilities['name']}: {e}")

    finally:
        driver.quit()
    
    # Get word counts from the translated titles
    word_counts = get_word_counts(translated_titles)

    # Identify words that appear more than twice
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    # Print repeated words and their counts
    if repeated_words:
        print("Repeated words across translated titles:")
        for word, count in repeated_words.items():
            print(f"{word}: {count}")
    else:
        print("No words repeated more than twice.")

# Run tests in parallel
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_test, capabilities) for capabilities in capabilities_list]
        for future in futures:
            future.result()


# # BrowserStack capabilities for 5 different browsers/devices
# capabilities_list = [
#     {
#         "browserName": "Chrome",
#         "browserVersion": "latest",
#         "os": "Windows",
#         "osVersion": "10",
#         # "name": "Chrome Test",
#         "build": "Parallel Tests",
#         "browserstack.debug": True,
#         "browserstack.networkLogs": True,
#     },
#     {
#         "browserName": "Firefox",
#         "browserVersion": "latest",
#         "os": "Windows",
#         "osVersion": "10",
#         # "name": "Firefox Test",
#         "build": "Parallel Tests",
#         "browserstack.debug": True,
#         "browserstack.networkLogs": True,
#     },
#     {
#         "browserName": "Safari",
#         "browserVersion": "latest",
#         "os": "OS X",
#         "osVersion": "Ventura",
#         # "name": "Safari Test",
#         "build": "Parallel Tests",
#         "browserstack.debug": True,
#         "browserstack.networkLogs": True,
#     },
#     {
#         "browserName": "Edge",
#         "browserVersion": "latest",
#         "os": "Windows",
#         "osVersion": "10",
#         # "name": "Edge Test",
#         "build": "Parallel Tests",
#         "browserstack.debug": True,
#         "browserstack.networkLogs": True,
#     },
#     # {
#     #     "device": "Samsung Galaxy S23",
#     #     "os_version": "13.0",
#     #     "realMobile": True,
#     #     # "name": "Mobile Test",
#     #     "build": "Parallel Tests",
#     #     "browserstack.debug": True,
#     #     "browserstack.networkLogs": True,
#     # },
# ]

# driver = webdriver.Remote(
#     command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
#     desired_capabilities={
#         "browserName": capabilities["browserName"],
#         "browserVersion": capabilities["browserVersion"],
#         "os": capabilities["os"],
#         "osVersion": capabilities["osVersion"],
#         "build": capabilities.get("build", "Default Build"),
#         "name": capabilities.get("name", "Default Test"),
#         "browserstack.user": BROWSERSTACK_USERNAME,
#         "browserstack.key": BROWSERSTACK_ACCESS_KEY,
#         "browserstack.debug": True,
#         "browserstack.networkLogs": True,
#     }
# )

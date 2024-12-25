import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import Counter
import re
import os

# Path to your ChromeDriver
CHROME_DRIVER_PATH = "drivers/chromedriver"  # Update with the exact path to your ChromeDriver

# Get the parent directory of the src folder
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the path to the article_images folder
article_images = os.path.join(parent_directory, 'article_images')

# Ensure the article_images directory exists
os.makedirs(article_images, exist_ok=True)

# RapidAPI credentials
api_url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
api_key = "993fa7ed9amsh7c3b7004ccdefd6p147216jsnfddc6eaac794"  # Replace with your RapidAPI key

# Set up headers for the API request
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "rapid-translate-multi-traduction.p.rapidapi.com",
    "Content-Type": "application/json"
}

# Function to use Rapid Translate API
def translate_text(text, source_lang='es', target_lang='en'):
    params = {
        "from": source_lang,
        "to": target_lang,
        "q": [text]
    }
    
    response = requests.post(api_url, json=params, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"API Response: {result}")
        
        # Handling if the response is a list or dictionary
        if isinstance(result, list):
            return result[0]
        else:
            return result['translated_text']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return text

# Function to tokenize and count word frequencies
def get_word_counts(text_list):
    word_counts = Counter()
    for text in text_list:
        # Tokenize the text by splitting on non-alphanumeric characters and convert to lowercase
        words = re.findall(r'\b\w+\b', text.lower())
        word_counts.update(words)
    return word_counts

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))

# List to store translated titles
translated_titles = []

try:
    # Navigate to the website's Opinion section
    base_url = "https://elpais.com"
    opinion_section_url = f"{base_url}/opinion"
    driver.get(opinion_section_url)

    # Wait for the page to load and ensure articles are present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))

    # Fetch the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    # Locate the articles in the Opinion section
    articles = soup.find_all("article", limit=5)  # Fetch the first 5 articles
    if not articles:
        print("No articles found in the Opinion section.")
        driver.quit()
        exit()

    # Create a folder to save images
    image_folder = "article_images"
    os.makedirs(image_folder, exist_ok=True)

    # Loop through the articles
    for idx, article in enumerate(articles, start=1):
        try:
            # Extract title
            title_tag = article.find("h2") or article.find("h3")
            title = title_tag.text.strip() if title_tag else "No title found"
            print(title)

            # Translate the title to English using Rapid Translate
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
                    image_url = image_tag["src"]

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
            print(f"Error processing Article {idx}: {e}")

finally:
    # Quit the WebDriver
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

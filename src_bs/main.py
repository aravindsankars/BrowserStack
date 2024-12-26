from config import Config
from translator import Translator
from scraper import Scraper
from utilities import Utilities
from concurrent.futures import ThreadPoolExecutor
import os
from urllib.parse import urljoin

def run_test(config, translator, scraper, capabilities):
    driver = scraper.create_driver(capabilities)
    try:
        articles = scraper.fetch_articles(driver)
        translated_titles = []

        for idx, article in enumerate(articles, start=1):
            title_tag = article.find("h2") or article.find("h3")
            title = title_tag.text.strip() if title_tag else "No title found"
            print(title)

            # Translate title
            translated_title = translator.translate_text(title)

            # Ensure translated_title is valid
            if translated_title:
                print(translated_title)
                translated_titles.append(translated_title)
            
            # Extract content
            content_tags = article.find_all("p")
            content = " ".join(tag.text.strip() for tag in content_tags) if content_tags else "No content found"
            print(content)

            # Save images
            image_tag = article.find("img")
            if image_tag and "src" in image_tag.attrs:
                scraper.save_image(urljoin("https://elpais.com/opinion", image_tag["src"]),
                                   os.path.join(config.get_article_images_path(), f"article_{idx}_cover.jpg"))

        # Word count analysis
        if translated_titles:
            word_counts = Utilities.get_word_counts(translated_titles)
            repeated_words = {word: count for word, count in word_counts.items() if count > 2}
            if repeated_words:
                print("Repeated words:", repeated_words)
            else:
                print("No repeated words!")
        else:
            print("No valid translated titles found.")


    finally:
        driver.quit()

if __name__ == "__main__":
    config = Config()
    translator = Translator(*config.get_rapidapi_credentials())
    scraper = Scraper(*config.get_browserstack_credentials(), config.get_article_images_path())

    capabilities_list = config.get_capabilities()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_test, config, translator, scraper, capabilities) for capabilities in capabilities_list]
        for future in futures:
            future.result()

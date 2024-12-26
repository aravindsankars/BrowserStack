from config import Config
from translate import Translator
from scraper_local import Scraper
from utilities import get_word_counts
import os

def main():
    # Load configuration
    
    config = Config("secrets.yml")
    article_images_path = config.get_article_images_path()

    # Initialize translator and scraper
    translator = Translator(*config.get_rapidapi_credentials())
    scraper = Scraper(driver_path="drivers/chromedriver", base_url="https://elpais.com")

    try:
        # Fetch articles
        articles = scraper.fetch_articles()
        translated_titles = []

        for idx, article in enumerate(articles, start=1):
            title_tag = article.find("h2") or article.find("h3")
            title = title_tag.text.strip() if title_tag else "No title found"
            print(title)
            
            # Translate the title
            translated_title = translator.translate_text(title)
            
            # Ensure translated_title is valid
            if translated_title:
                print(translated_title)
                translated_titles.append(translated_title)

            # Extract content
            content_tags = article.find_all("p")
            content = " ".join(tag.text.strip() for tag in content_tags) if content_tags else "No content found"
            print(content)

            # Attempt to find and save the article's image
            image_tag = article.find("img")
            if image_tag and "src" in image_tag.attrs:
                scraper.save_image(image_tag["src"], os.path.join(article_images_path, f"article_{idx}_cover.jpg"))

        # Analyze word counts only for non-empty translated titles
        if translated_titles:
            word_counts = get_word_counts(translated_titles)
            repeated_words = {word: count for word, count in word_counts.items() if count > 2}
            if repeated_words:
                print("Repeated words:", repeated_words)
            else:
                print("No repeated words!")
        else:
            print("No valid translated titles found.")

    finally:
        scraper.quit()

if __name__ == "__main__":
    main()


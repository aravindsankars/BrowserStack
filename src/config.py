import os
import yaml

class Config:
    def __init__(self, secrets_path="secrets.yml"):
        with open(secrets_path, "r") as file:
            self.config = yaml.safe_load(file)

    @property
    def rapid_api_key(self):
        return self.config['secrets']['rapid_api_key']

    @property
    def rapid_api_url(self):
        return self.config['secrets']['rapid_api_url']

    @staticmethod
    def get_article_images_path():
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        article_images = os.path.join(parent_directory, 'article_images')
        os.makedirs(article_images, exist_ok=True)
        return article_images

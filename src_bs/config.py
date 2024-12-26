import os
import yaml

class Config:
    def __init__(self, secrets_file="secrets.yml", bs_file="browserstack.yml"):
        with open(secrets_file, "r") as file:
            self.secrets = yaml.safe_load(file)
        
        with open(bs_file, "r") as file:
            self.bs_config = yaml.safe_load(file)
        
        # Define paths
        self.parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.article_images_path = os.path.join(self.parent_directory, 'article_images')
        os.makedirs(self.article_images_path, exist_ok=True)

    def get_browserstack_credentials(self):
        return self.secrets['secrets']['browserstack_username'], self.secrets['secrets']['browserstack_access_key']

    def get_rapidapi_credentials(self):
        return self.secrets['secrets']['rapid_api_key'], self.secrets['secrets']['rapid_api_url']

    def get_capabilities(self):
        return self.bs_config['platforms']

    def get_article_images_path(self):
        return self.article_images_path

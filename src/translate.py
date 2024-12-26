import requests

class Translator:
    def __init__(self, api_key, api_url):
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "rapid-translate-multi-traduction.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        self.api_url = api_url

    def translate_text(self, text, source_lang='es', target_lang='en'):
        params = {"from": source_lang, "to": target_lang, "q": [text]}
        response = requests.post(self.api_url, json=params, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            return result[0] if isinstance(result, list) else result['translated_text']
        else:
            print(f"Error: {response.status_code}")
            return None

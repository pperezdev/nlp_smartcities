import requests
from bs4 import BeautifulSoup

class Extractor:
    def __init__(self) -> None:
        pass
    
    def extract_wikipedia(self, url):
        pass
        
    def extract(self, url:str):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup.get_text()
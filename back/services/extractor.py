import requests
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment

class Document:
    def __init__(self, title, content) -> None:
        self.title = title
        self.content = content
        self.date = datetime.now()

class Extractor:
    def __init__(self) -> None:
        pass
    
    def extract_wikipedia_link(self, url) -> list[Document]:
        documents = list[Document]
        page = requests.get(url)
        for link in BeautifulSoup(page, parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                print(link['href'])
                
        return documents
    
    def tag_visible(self, element) -> bool:
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True


    def extract(self, url:str) -> Document:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.title.get_text()
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts) 
        content = u" ".join(t.strip() for t in visible_texts)
        return Document(title,content )
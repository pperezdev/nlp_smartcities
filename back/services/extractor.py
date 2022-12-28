import requests
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer
from tqdm import tqdm
from bs4.element import Comment
import uuid

class Document:
    def __init__(self, title:str=None, content:str=None, id:uuid=None, extension:str='txt') -> None:
        self.id = id
        if id == None:
            self.id = uuid.uuid1()
            
        self.extension = extension
        self.title = title
        self.content = content
        self.date = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'id':str(self.id),
            'document': f"{self.title}.{self.extension}",
            'date':self.date.strftime("%d-%m-%YT%H:%M:%SZ%f")
        }

class Extractor:
    def __init__(self) -> None:
        self.startwith_test_0 = "https"
        self.startwith_test_1 = "/wiki"
    
    def tag_visible(self, element) -> bool:
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True


    def clean_title(self, soup:BeautifulSoup) -> str:
        title_raw = soup.title.get_text()
        title_raw = title_raw.replace("\n", "")
        title_raw = title_raw.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=+"})
        title = title_raw.replace(' ', '_').lower()
        return title
    
    def clean_link(self, soup:BeautifulSoup) -> list[str]:
        link_url = []
        for link in soup.find_all('a'):
            link_raw = str(link.get('href'))
            if link_raw.startswith(self.startwith_test_0) or link_raw.startswith(self.startwith_test_1):
                if link_raw.startswith(self.startwith_test_1):
                    link_raw = f"https://wikipedia.org{link_raw}"
                link_url.append(link_raw)
        return link_url
    
    def extract_wikipedia(self, url:str) -> list[Document]:
        documents = []
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        documents.append(self.extract(url))
        link_url = self.clean_link(soup)
        
        for link in tqdm(link_url):
            try:
                documents.append(self.extract(link))
            except:
                print(f"ERROR AT: {link}")
        
        return documents

    def extract(self, url:str) -> Document:
        
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        title = self.clean_title(soup)
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts) 
        content = u" ".join(t.strip() for t in visible_texts)
        
        return Document(title,content)
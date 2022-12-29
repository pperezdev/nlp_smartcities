import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from bs4.element import Comment
from .result_error import Result
import os
from .file_manager import FileManagers
from .document import Document

class Extractor:
    def __init__(self) -> None:
        self.fm = FileManagers()
        self.size_min = 5000
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
    
    def extract_wikipedia(self, url:str) -> Result:
        documents = []
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        result_0 = self.extract(url)
        if result_0.error == False:
            documents.append(result_0.data)
            
        link_url = self.clean_link(soup)
        
        for link in tqdm(link_url):
            
            result_1 = self.extract(link)
            if result_1.error == False:
                documents.append(result_1.data)

        return Result(documents, False)

    def download_pdf_file(self, url: str) -> Result:
        response = requests.get(url, stream=True)

        pdf_file_name = os.path.basename(url).split('.')[0]
        if response.status_code == 200:
            doc = Document(pdf_file_name, response.content,extension="pdf",encoding=None, type='byte')
            self.fm.write_document(doc)
            return Result(pdf_file_name, False)
        else:
            return Result(None, True)
        
    def extract_pdf(self, url:str) -> Result:
        result = self.download_pdf_file(url)
        if result.error == True:
            return Result(None, True)
        
        result_2 = self.fm.read_pdf(result.data)
        if result_2.error == True:
            return Result(None, True)
        
        doc = Document(result.data, result_2.data)
        return Result(doc, False)
        
    def extract(self, url: str) -> Result :        
        if url.endswith('.pdf'):
            return self.extract_pdf(url)
        return self.extract_web(url)
            
    def extract_web(self, url:str) -> Result:
        doc = None
        error = True
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            title = self.clean_title(soup)
            texts = soup.findAll(text=True)
            visible_texts = filter(self.tag_visible, texts) 
            content = u" ".join(t.strip() for t in visible_texts)
            
            if len(content) > self.size_min:
                doc = Document(title,content)
                error = False
        except:
            print(f"ERROR AT: {url}")
            
        return Result(doc, error)
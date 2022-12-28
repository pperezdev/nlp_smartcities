from back.services import *

class ExtractDocument:
    def __init__(self) -> None:
        self.file_manager = FileManagers() 
        self.extractor = Extractor()
        
    def extract(self, url) -> Document:
        return self.extractor.extract(url)
    
    def extract_wikipedia(self, url) -> Document:
        return self.extractor.extract_wikipedia(url)
        
    def write_document(self, url:str, wikipedia:bool=False):
        doc = Document()
        if wikipedia:
            doc = self.extract_wikipedia(url)
            self.file_manager.write_document_list(doc)
        else:
            doc = self.extract(url)
            self.file_manager.write_document(doc)
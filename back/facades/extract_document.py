from back.services import *

class ExtractDocument:
    def __init__(self) -> None:
        self.file_manager = FileManagers() 
        self.extractor = Extractor()
        
    def extract(self, url) -> Result:
        return self.extractor.extract(url)
    
    def extract_wikipedia(self, url) -> Result:
        return self.extractor.extract_wikipedia(url)
        
    def write_document(self, url:str, wikipedia:bool=False):
        if wikipedia:
            result = self.extract_wikipedia(url)
            if result.error == False:
                self.file_manager.write_document_list(result.data)
        else:
            result = self.extract(url)
            if result.error == False:
                self.file_manager.write_document(result.data)
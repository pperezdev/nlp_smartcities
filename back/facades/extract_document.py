from services import FileManagers, Extractor, Document

class ExtractDocument:
    def __init__(self) -> None:
        self.file_manager = FileManagers() 
        self.extractor = Extractor()
        
    def extract(self, url) -> Document:
        return self.extractor.extract(url)
        
    def write_document(self, url):
        self.file_manager.write_data(self.extract(url))
    
    
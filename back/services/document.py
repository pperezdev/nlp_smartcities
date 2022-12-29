from datetime import datetime
import uuid

class Document:
    def __init__(self, title:str=None, content:str=None, id:uuid=None, extension:str='txt', encoding="utf-8", type="text") -> None:
        self.id = id
        if id == None:
            self.id = uuid.uuid1()
            
        self.extension = extension
        self.encoding = encoding
        self.title = title
        self.content = content
        self.date = datetime.now()
        self.type = type
        self.w_method = ''
        if type == "text":
            self.w_method = 'w+'
        elif type == "byte":
            self.w_method = 'wb'
            
    def to_dict(self) -> dict:        
        return {
            'id':str(self.id),
            'document': f"{self.title}.{self.extension}",
            'encoding': str(self.encoding),
            'type' : self.type,
            'date':self.date.strftime("%d-%m-%YT%H:%M:%SZ%f")
        }
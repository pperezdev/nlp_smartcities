import pickle
import io
import nltk
import os
import codecs
import json
import uuid
from werkzeug.datastructures import FileStorage
from .document import Document
from .result_error import Result
import pypdf

class FileManagers:
    def __init__(self) -> None:
        basedir = os.path.dirname(os.path.abspath(__file__))[:-13]
        self.main_path = f"{basedir}data"
    
    def open_file(self, fct, file_name:str, follow_path:str, end_file:str, write_method:str='wb', encoding:str=None, *args, **kwargs) -> Result:
        val = None
        error = True
        
        path = f"{self.main_path}/{follow_path}/{file_name}.{end_file}"
   
        with codecs.open(path, write_method, encoding=encoding) as file:
            result = fct(file, *args, **kwargs)
            if result.error == False:
                val = result.data
                error = False
            
        return Result(val, error)
    
    def __write_document_byte(self, file:io.BufferedWriter, byte:bytes, *args, **kwargs) -> Result:
        file.write(byte)
        return Result(None, False)
    
    def __write_document(self, file:io.BufferedWriter, text:str, *args, **kwargs) -> Result:
        file.write(text)
        return Result(None, False)
    
    def __write_document_json(self, file:io.BufferedWriter, dictionary:dict, *args, **kwargs) -> Result:
        json.dump(dictionary, file)
        return Result(None, False)
    
    def __load_model(self, file:io.BufferedWriter, *args, **kwargs) -> Result:
        val = pickle.load(file)
        return Result(val, False)
        
    def __save_model(self, file:io.BufferedWriter, classifier:nltk.NaiveBayesClassifier, *args, **kwargs) -> Result:
        pickle.dump(classifier, file)
        return Result(None, False)
    
    def __read_document(self, file:io.BufferedWriter, *args, **kwargs)-> Result:
        content = file.read()
        return Result(content, False)
        
    def __read_pdf(self, file:io.BufferedWriter, *args, **kwargs)-> Result:
        try:
            pdf_reader = pypdf.PdfReader(file)
            content = ""
            
            for page in pdf_reader.pages:
                content += page.extract_text()
            
            return Result(content, False)
        except:
            return Result(None, True)
    
    def file_save(self, file:FileStorage, file_name:str) -> Result:
        path = f"{self.main_path}/uploads/{file_name}"
        file.save(path)
        
        return Result(file_name.split('.')[0], False)
    
    def write_datanode(self, document:Document, type:str) -> Result:
        id = uuid.uuid1()
        title = f"DATANODE-{type}-{id}"
        return self.open_file(self.__write_document_json, title, "datanodes", "json", 'w+', 'utf-8', document.to_dict())
    
    def write_document_list(self, documents:list[Document]) -> Result:
        result_list = []
        result = Result(result_list, False)
        
        for document in documents:
            result.data.append(self.write_document(document))
    
        return result
    
    def write_document(self, document:Document) -> Result:
        result_list = []
        result = Result(result_list, False)
        fct = self.__write_document
        if document.type == 'byte':
            fct = self.__write_document_byte
        
        result_0 = self.open_file(fct, document.title, "datasets", document.extension, document.w_method, document.encoding, document.content)
        result.data.append(result_0)
        if result_0.error == False:
            result.data.append(self.write_datanode(document, "DATA"))
        return result
    
    def load_model(self, file_name:str) -> Result:
        return self.open_file(self.__load_model, file_name, "models", "pickle")
        
    def save_model(self, file_name:str, classifier:nltk.NaiveBayesClassifier) -> Result:
        return self.open_file(self.__save_model, file_name, "models", "pickle", 'w+', classifier)
    
    
    def read_pdf(self, file_name:str, follow_path:str="datasets") -> Result:
        return self.open_file(self.__read_pdf, file_name, follow_path, 'pdf', 'rb')
    
    def read_document(self, file_name:str) -> Result:
        return self.open_file(self.__read_document, file_name, "datasets", 'txt', 'r+','utf-8')
    
    def read_documents() -> list[Document]:
        pass
    
    def get_models_name_list(self) -> list[str]:
        model_name = list[str]
        path = f"{self.main_path}/models/"
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                model_name.append(file.split('.')[0])
        return model_name
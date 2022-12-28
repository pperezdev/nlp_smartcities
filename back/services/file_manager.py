import pickle
import io
import nltk
import os
import codecs
import json
import uuid
from .extractor import Document

class Result:
    def __init__(self, data, result:str) -> None:
        self.data = data
        self.result = result

class FileManagers:
    def __init__(self) -> None:
        basedir = os.path.dirname(os.path.abspath(__file__))[:-13]
        self.main_path = f"{basedir}data"
    
    def open_file(self, fct, file_name:str, follow_path:str, end_file:str, write_method:str='wb', *args, **kwargs) -> Result:
        val = "error"
        path = f"{self.main_path}/{follow_path}/{file_name}.{end_file}"
        with codecs.open(path, write_method, "utf-8") as file:
            val = fct(file, *args, **kwargs)
        return Result(val, "")
    
    def __write_document(self, file:io.BufferedWriter, text:str, *args, **kwargs) -> object:
        file.write(text)
        return None
    
    def __write_document_json(self, file:io.BufferedWriter, dictionary:dict, *args, **kwargs) -> object:
        json.dump(dictionary, file)
        return None
    
    def __load_model(self, file:io.BufferedWriter, *args, **kwargs) -> object:
        return pickle.load(file)
        
    def __save_model(self, file:io.BufferedWriter, classifier:nltk.NaiveBayesClassifier, *args, **kwargs) -> object:
        pickle.dump(classifier, file)
        return None
    
    def write_datanode(self, document:Document, type:str) -> Result:
        id = uuid.uuid1()
        title = f"DATANODE-{type}-{id}"
        return self.open_file(self.__write_document_json, title, "datanodes", "json", 'w+', document.to_dict())
    
    def write_document_list(self, documents:list[Document]) -> Result:
        result_list = []
        result = Result(result_list, "")
        
        for document in documents:
            result.data.append(self.write_document(document))
    
        return result
    
    def write_document(self, document:Document) -> Result:
        result_list = []
        result = Result(result_list, "")
        result.data.append(self.open_file(self.__write_document, document.title, "datasets", document.extension, 'w+', document.content))
        result.data.append(self.write_datanode(document, "DATA"))
        return result
    
    def load_model(self, file_name:str) -> Result:
        return self.open_file(self.__load_model, file_name, "models", "pickle")
        
    def save_model(self, file_name:str, classifier:nltk.NaiveBayesClassifier) -> Result:
        return self.open_file(self.__save_model, file_name, "models", "pickle", 'w+', classifier)
    
    def load_Documents() -> list[Document]:
        pass
    
    def get_models_name_list(self) -> list[str]:
        model_name = list[str]
        path = f"{self.main_path}/models/"
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                model_name.append(file.split('.')[0])
        return model_name
import pickle
import io
import nltk
import os
import codecs

class Result:
    def __init__(self, data:object, result:str) -> None:
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
    
    def __write_data(self, file:io.BufferedWriter, text:str, *args, **kwargs) -> object:
        file.write(text)
        return None
    
    def __load_model(self, file:io.BufferedWriter, *args, **kwargs) -> object:
        return pickle.load(file)
        
    def __save_model(self, file:io.BufferedWriter, classifier:nltk.NaiveBayesClassifier, *args, **kwargs) -> object:
        pickle.dump(classifier, file)
        return None
    
    def write_data(self, file_name:str, text:str) -> Result:
        return self.open_file(self.__write_data, file_name, "datasets", "txt", 'w+', text)
    
    def load_model(self, file_name:str) -> Result:
        return self.open_file(self.__load_model, file_name, "models", "pickle")
        
    def save_model(self, file_name:str, classifier:nltk.NaiveBayesClassifier) -> Result:
        return self.open_file(self.__save_model, file_name, "models", "pickle", 'w+', classifier)
    
    def get_models_name_list(self) -> list[str]:
        model_name = list[str]
        path = f"{self.main_path}/models/"
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                model_name.append(file.split('.')[0])
        return model_name
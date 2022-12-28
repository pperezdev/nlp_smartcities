import pickle
import io
import nltk

class Result:
    def __init__(self, data:object, result:str) -> None:
        self.data = data
        self.result = result

class FileManagers:
    def __init__(self) -> None:
        self.main_path = "./data/"
    
    def open_file(self, fct:function, file_name:str, follow_path:str, end_file:str, *args, **kwargs) -> Result:
        val = "error"
        path = f"{self.main_path}/{follow_path}/{file_name}.{end_file}"
        with open(path, 'wb') as file:
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
        return self.open_file(self.__write_data, file_name, "datasets", "txt", text)
    
    def load_model(self, file_name:str) -> Result:
        return self.open_file(self.__load_model, file_name, "models", "pickle")
        
    def save_model(self, file_name:str, classifier:nltk.NaiveBayesClassifier) -> Result:
        return self.open_file(self.__save_model, file_name, classifier, "models", "pickle")
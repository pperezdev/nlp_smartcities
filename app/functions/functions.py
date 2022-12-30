from back import FileManagers, Document
from werkzeug.datastructures import FileStorage

def get_models_name() -> list[str]:
    fm = FileManagers()
    return fm.get_models_name_list()

def get_synthesis_url(model_name:str, url:str) -> str:
    fm = FileManagers()
    #LANCER LA FONCTION SYNTHESE
    return ""

def get_synthesis_text(model_name:str, text:str) -> str:
    #LANCER LA FONCTION SYNTHESE
    synth = text[20:100]
    return synth

def get_synthesis_pdf(file:FileStorage , filename:str) -> str:
    fm = FileManagers()
    result = fm.file_save(file, filename)
    if result.error == True:
        return "Error file"
    
    result_2 = fm.read_pdf(result.data, follow_path="uploads")
    
    if result_2.error == True:
        return "Error file"
        
    doc = Document(result.data, result_2.data)
    content = doc.content
    
    #LANCER LA FONCTION SYNTHESE
    synth = content[20:100]
    print(content)
    
    return synth
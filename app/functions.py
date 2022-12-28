from back import FileManagers

def get_models_name() -> list(str):
    fm = FileManagers()
    return fm.get_models_name_list()

def get_synthesis_url(model_name:str, url:str) -> str:
    return ""

def get_synthesis_text(model_name:str, text:str) -> str:
    return ""
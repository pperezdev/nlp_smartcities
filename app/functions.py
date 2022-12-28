from back.file_manager import FileManagers

def get_models_name() -> list(str):
    fm = FileManagers()
    return fm.get_models_name_list()

def select_model(model_name:str):
    pass
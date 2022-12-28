from back.extractor import Extractor
from back.file_manager import FileManagers
ext = Extractor()

url = "https://en.wikipedia.org/wiki/Smart_city"

ext.extract(url)


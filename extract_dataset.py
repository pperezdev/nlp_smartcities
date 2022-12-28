from back import Extractor
from back import FileManagers
ext = Extractor()

url = "https://en.wikipedia.org/wiki/Smart_city"

fm = FileManagers() 
fm.write_data(ext.extract(url))


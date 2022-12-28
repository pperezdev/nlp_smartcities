from back import ExtractDocument
ext_doc = ExtractDocument()

url = "https://en.wikipedia.org/wiki/Smart_city"

ext_doc.write_document(url, wikipedia=True)


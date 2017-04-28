import pytesseract
from docx import opendocx, getdocumenttext
import subprocess
import os
import textract
try:
    import Image
except ImportError:
    from PIL import Image
from docx import opendocx, getdocumenttext
# Uses antiword to convert a .doc file into text
def parse_doc(full_path):
    fullpath = "../" + full_path
    parsed_doc = subprocess.check_output(["antiword", "-t", fullpath], cwd="antiword", shell=True)
    return parsed_doc

# Uses docx to convert a .docx file into text
def parse_docx(full_path):
    fullpath = "../" + full_path
    document = opendocx(full_path)
    paratextlist = getdocumenttext(document)
    newparatextlist = []
    for paratext in paratextlist:
        newparatextlist.append(paratext.encode("utf-8"))
    return '\n\n'.join(newparatextlist)

# Uses Pdfminer to convert a pdf to into text
def parse_pdf(full_path):
    fullpath = "../" + full_path
    parsed_pdf = subprocess.check_output(["python", "tools/pdf2txt.py", fullpath], cwd="pdfminer", shell=True)
    return parsed_pdf


# Uses pytesseract to convert an image into text
def ocr(full_path):
    fullpath = full_path
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
    my_path = os.path.abspath(__file__)
    mydir = os.path.dirname(my_path)
    return pytesseract.image_to_string(Image.open(fullpath))

def odt(full_path):
    return textract.process(full_path)


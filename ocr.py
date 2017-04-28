import os
import pytesseract
try:
    import Image
except ImportError:
    from PIL import Image
#Must install https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
my_path = os.path.abspath(__file__)
mydir = os.path.dirname(my_path)
start = os.path.join(mydir, "img002.jpg")
#print start
#print(pytesseract.image_to_string(Image.open(start)))
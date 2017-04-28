# JANUS (Email Extractor)

Janus (Email Extractor) is a python application that assists the Governments policy consultation process by extracting answers to questions from both emails (Outlook files) and survey responses (SmartSurvey). Email responses are parsed for all textual content, this includes all attachments. Once the text has been parsed it can be run through the built-in NLP engine to extract answers to the list of questions which were asked as part of the consultation.

# Getting Started

  - Setup a MongoDB database and collection
  - Export all relevant emails in Outlook as .msg files to the folder named "Data"
  - Fill out correct SmartSurvey and MongoDB credentials in the secrets.py file
  - Install dependencides:
  ```sh
pip install -r requirements.txt
```
  - Run the Email Extractor:
```sh
python email_extractor.py
```

### Dependencies

Dillinger uses a number of open source projects to work properly:

* [Pytesseract] - Python-tesseract is a python wrapper for google's Tesseract-OCR.
* [Docx] - The docx module creates, reads and writes Microsoft Office Word 2007 docx files
* [textract] - Extract text from any document. No muss. No fuss.
* [Pymongo] - The Python driver for MongoDB
* [Fuzzywuzzy] - Fuzzy String Matching in Python
* [NLTK] - Natural Language Toolkit


import os, re, glob, subprocess, shutil, json, openpyxl, parsers, PIL, mongodb, SmartSurvey, new_nlp, os, bson, hashlib
#pip install python-Levenshtein


print("Started OK...  \n")

def organise_emails_numerically():
    """Takes all emails in the data folder and
        renames them numerically incrementing.
    """
    numbericName = 0
    root = 'data'
    for filename in os.listdir(root):
        if filename.endswith(".msg"):
            newName = str(numbericName) + ".msg"
            try:
                os.rename(os.path.join(root, filename), os.path.join(root, newName))
                print filename + " to " + newName
                os.remove(filename)
            except WindowsError:

                numbericName += 1
                pass
    print("All "+ str(numbericName) +" Message Files Have Been Renamed Numerically \n")


def extract_data_from_emails():
    """Extracts all .msg files in the data folder and then
        moves the output folders into the data/Processed folder
    """
    #loops for each .msg file
    for message in glob.glob('./data/*.msg'):
        print "Extracting - " + message
        #Calls the ExtractMsg script within the data folder to execute on each .msg file
        subprocess.call(["python", "ExtractMsg.py", "--json", os.path.basename(message)], cwd="data", shell=True)
    #Generates a file directory
    root, dirs, files = os.walk("data").next()
    nameCount = 0
    #Iterates through all directories in data folder
    for dir in dirs:

        #Renames the folder with a numerical name
        os.rename(os.path.join(root, dir), os.path.join(root, str(nameCount)))
        # Moves the folder to the data/Processed folder
        shutil.move(os.path.join(root, str(nameCount)), "data/Processed/")
        nameCount += 1


def seek_through_emails(id):
    """Loops through all emails and builds an array
    """
    directory = "data/Processed/" + str(id) + "/"

    try:
        folders =  os.walk(directory).next()[2]
        files_array = []
        for files in folders:
            files_array.append(files)
        return files_array
    except StopIteration:
        print("Interation Fail")

# Identifies the file type
# @param file_name <desc>
# @return <desc>
def identify_filetype(file_name):
    """Extracts the file extension from a filename
    """
    filename, file_extension = os.path.splitext(file_name)
    return file_extension

def parse(id,attachments):
    """Parses document depending on the file extension
    """
    path = "data/Processed/" + str(id) + "/"
    data = []
    try:
        for attachment in attachments:
            full_path = path + str(attachment)
            if identify_filetype(attachment) == ".doc":
                data.append(parsers.parse_doc(full_path))
            if identify_filetype(attachment) == ".docx":
                data.append(parsers.parse_docx(full_path))
            if identify_filetype(attachment) == ".png" or identify_filetype(attachment) == ".jpg" \
            or identify_filetype(attachment) == ".jpeg":
                data.append(parsers.ocr(full_path))
            if identify_filetype(attachment) == ".pdf":
                data.append(parsers.parse_pdf(full_path))
            if identify_filetype(attachment) == ".odt":
                data.append(parsers.odt(full_path))
    except TypeError:
        print("Error")
    return data



def initalize_worksheet():
    """This function opens up the worksheet.
    """


def purge_processed():
    folder = 'data/Processed/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print("Error: " + str(e))

def process_emails():
    list = os.listdir("data/Processed/") # dir is your directory path
    folder = 'data/Processed/'
    emails = len(list)
    count = 0
    md5s = []
    print str(emails) + " to be processed"
    while count < emails:
        adjusted_email_count = count + 1
        path = "data/Processed/" + str(adjusted_email_count) + "/message.json"
        try:
            md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
        except IOError:
            print "test"


        print(str(adjusted_email_count) +  "/" + str(emails)+ " being processed")
        if md5 in md5s:
            print "Duplicate"
        else:

            md5s.append(md5)
            parse_json_email(count)
        count = count +1
    print("\n Emails processed")



# Takes the ID of an email and parses the data of the email.
def parse_json_email(id):
    data = {}
    regex = re.compile('[^a-zA-Z]')
    path = "data/Processed/" + str(id) + "/message.json"
    print("     Parsing " + path)
    files_array = seek_through_emails(id)
    attachment_content = parse(id, files_array)
    try:
        with open(path) as json_data:
            #print json_data
            parsed_json = json.load(json_data)
            #print parsed_json
            #print parsed_json['date']
            attachmentCount = 0
            if attachmentCount < len(parsed_json['attachments']):

                attachmentCount = + 1



            attachmentCount = len(parsed_json['attachments'])
            attachment_filetype = {}
            decoded_attachment = {}
            data["date"] = parsed_json['date']
            data["subject"] = parsed_json['subject']
            data["from"] = parsed_json['from']
            data["to"] = parsed_json['to']
            data["cc"] = parsed_json['cc']
            data["body"] = remover(parsed_json['body'])

            data["attachmentCount"] = len(parsed_json['attachments'])
            data["md5"] = hashlib.md5(open(path, 'rb').read()).hexdigest()
            #print parsed_json

            counter = 0
            print "     Attachments: " + str(attachmentCount)
            while counter < attachmentCount:

                currentlyprocessing = counter + 1
                print "     Attachment " + str(currentlyprocessing) + " of " +  str(attachmentCount)
                attachment_filetype[counter] = identify_filetype(parsed_json['attachments'][counter])
                data["attachment" + str(currentlyprocessing) + "Type"] = attachment_filetype[counter]


                counter = counter + 1


            parsed_json['to'] = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', repr(parsed_json['to']))

            try:



                standard = [parsed_json['date'], parsed_json['subject'], parsed_json['from'], parsed_json['to'],
                            parsed_json['cc'],
                            parsed_json['body'], len(parsed_json['attachments'])]

                count = 0
                extra = []
                print "     Parsed Attachments " + str(len(parsed_json['attachments']))
                while count < len(attachment_content):
                    print count
                    #print attachment_content[count]

                    attachment_content[count]  = attachment_content[count].replace("\n", "");
                    attachment_content[count] = attachment_content[count].replace("\r", "");
                    attachment_content[count] = attachment_content[count].replace("\f", "");

                    merged = standard
                    if attachment_content[count] == "":
                        attachment_content[count] = "N/A"
                    data["attachment" + str(currentlyprocessing) + "Content"] = attachment_content[count]
                    extra.append(parsed_json['attachments'][count])
                    extra.append(attachment_filetype[count])
                    extra.append(attachment_content[count])
                    question_answers =  new_nlp.extract_qa(attachment_content[count])
                    # question_answers
                    print "question answers sorted"

                    for qa in question_answers:
                        question = str(qa[4])
                        question = question.replace(".", "")
                        #data[question] = qa[3]
                        data["q"+str(qa[0])] = qa[3]

                    count = count + 1
                merged = standard + extra
                try:
                    pass
                   # ws.append(merged)
                    #print parsed_json['date']
                except openpyxl.utils.exceptions.IllegalCharacterError:
                    print "         Illegal character found - Content decoded"


            except IndexError:
                print("ERROR3")
            except openpyxl.utils.exceptions.IllegalCharacterError:
                print("         Illegal Character Error")
            #print data
            try:
                mongodb.insert_to_db(data)
            except bson.errors.InvalidStringData:
                pass
    except IOError:
        pass


def remover(text):
    # list of signatures to remove
    unwanted = [
        'visit our Web Site',
        'follow us',
        'watch us',
        'the information in this email',
        'sent from',
        'this email has been scanned',
        'this email and any attachments are intended',
        'if you have received this',
        'this e-mail',
        'disclaimer'
    ]

    # list of dft signatures
    dft_sign = [
        'night flights<mailto:',
        'night.flights@dft.gsi.gov.uk',
        '@dft.gsi.gov.uk',
        'great minster house',
        '33 horseferry road',
        'london, sw1p 4dr',
        'https://www.gov.uk/government',
        'https://www.',
        'gov.uk',
        'smartsurvey',
        'yours faithfully',
        'yours sincerely',
        'yours truly',
        'best regards',
        'kind regards',
        'best wishes',
        'warm regards',
        '\nsincerely',
        '\nregards',

    ]

    text = text.lower()

    # removing all text after signature
    for phrase in unwanted:
        if phrase in text:
            text, sep, tail = text.partition(phrase)

    # removing all dft signatures
    for phrase in dft_sign:
        if phrase in text:
            text = text.replace(phrase, '')

    return text
def run():

    mongodb.db_init()
    mongodb.empty_db()
    purge_processed()
    organise_emails_numerically()
    extract_data_from_emails()
    process_emails()
    purge_processed()
    SmartSurvey.extract_surevy_responses()



run()

















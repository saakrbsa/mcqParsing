
# PDF - TEXT

# PyPDF2

import encodings
from PyPDF2 import PdfFileReader
from pathlib import Path
import glob
import json
import re
import pymysql

for pdfFile in Path("pdfs").glob("*.pdf"):

# Create pdf file reader object

    pdf = PdfFileReader(pdfFile)

# Grab the page(s)

    page_1_object = pdf.getPage(0)

# Extract text

    page_1_text = page_1_object.extractText()


# Combine the text from all the pages and save as txt file

    with open("txts/{}.txt".format(pdfFile.stem), mode='w', encoding="utf-8") as file:
        for page in pdf.pages:
            text = ''
            text += page.extractText()
            file.write(text)
            file.close

# ---------------------------------------------------------------------------------------------------------------------- #

# TEXT - JSON

for txtFile in Path("txts").glob("*.txt"):

    with open(txtFile, 'r', encoding='utf-8') as file:

     data = file.read()

# Splits the questions into a list assuming there is no empty lines inside each question

    exam = re.split(r'\n', data)[0]
    subject = re.split(r'\n', exam)[0]
    questions = re.split(r'[1]+\.', data)[0]
    
    final_questions = []
    
    for question in questions:

# Extra check to make sure that this is a question

        if question != None and 'I.' in question:
         
         exam_name = exam.replace('\n','').rstrip()
         statement = re.split(r'[I]+\.', question)[0].replace('\n', '')
         option_a = re.split(r'[I]+\.', question)[1].replace('\n', '')
         option_b = re.split(r'[II]+\.', question)[1].replace('\n', '')

        #  option_a = re.findall(r'\ i\)\,[^ii]+\)+\,', question)[0].replace('\n', '')
        #  option_b = re.findall(r'\ i\i\)\,[^iii]+\)+\,', question)[0].replace('\n', '').rstrip()
        #  option_c = re.findall(r'\ i\i\i\)\,[^iv]+\)+\,', question)[0].replace('\n', '').rstrip()
        #  option_d = re.findall(r'\ i\v\)\,[^i]+\)+\,', question)[0].replace('\n', '').rstrip()

         final_questions.append({
                     'exam': exam_name,
                     'subject': subject,
                     'question': statement.strip(),
                     'option a': option_a.strip(),
                     'option b': option_b.strip(),
                     'option c': 0,
                     'option d': 0
                  })

    json_object = json.dumps(final_questions)

# Save JSON Files

    with open("jsons/{}.json".format(txtFile.stem), mode='w', encoding="utf-8") as file:

        file.write(json_object)
        file.close

# ---------------------------------------------------------------------------------------------------------------------- #

# JSON - MYSQL

con = pymysql.connect(host="localhost", user="root", password="00000000", database="mock_mcq")

cursor = con.cursor()

# cursor.execute("CREATE DATABASE mock_mcq")
cursor.execute("CREATE TABLE mockqns (id INT AUTO_INCREMENT PRIMARY KEY, exam VARCHAR(255), subject VARCHAR(255), questions VARCHAR(255),"
               "option_a VARCHAR(255), option_b VARCHAR(255), option_c VARCHAR(255), option_d VARCHAR(255),"
               "CONSTRAINT constr_id UNIQUE (exam,subject, questions))")

for JSONFile in Path("jsons").glob("*.json"):

    with open(JSONFile, 'r', encoding='utf8') as file:

        json_data = file.read()
        json_obj = json.loads(json_data)

    for items in json_obj:

        exam = items.get("exam")
        subject = items.get("subject")
        questions = items.get("question")
        option_a = items.get("option a")
        option_b = items.get("option b")
        option_c = items.get("option c")
        option_d = items.get("option d")
        cursor.execute("insert into mockqns(exam,subject,questions,option_a,option_b,option_c,option_d) value (%s,%s,%s,%s,%s,%s,%s)"
                       "ON DUPLICATE KEY UPDATE exam = exam;", (exam,subject,questions,option_a,option_b,option_c,option_d))
        con.commit()
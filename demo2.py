
# Read Multiple PDFs From One Folder And Write To Text Files In Another Folder

# PyPDF2

from PyPDF2 import PdfFileReader
from pathlib import Path
import glob
import json
import re

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

for txtFile in Path("txts").glob("*.txt"):

    with open(txtFile, 'r', encoding='utf8') as file:

     data = file.read()

# Splits the questions into a list assuming there is no empty lines inside each question

    questions = re.split(r'\n\s*\n', data)
    final_questions = []
    
    for question in questions:

# Extra check to make sure that this is a question

        if question != None and '(i)' in question:

         statement = re.findall(r'[^(]+', question)[0].replace('\n', '').rstrip()
         option_a = re.findall(r'\(i\)[^(]+', question)[0].replace('\n', '').rstrip()
         option_b = re.findall(r'\(ii\)[^(]+', question)[0].replace('\n', '').rstrip()
         option_c = re.findall(r'\(iii\)[^(]+', question)[0].replace('\n', '').rstrip()
         option_d = re.findall(r'\(iv\)[^(]+', question)[0].replace('\n', '').rstrip()

         final_questions.append({
                     'question': statement.rstrip(),
                      'option a': option_a,
                      'option b': option_b,
                      'option c': option_c,
                      'option d': option_d
                  })

    print(final_questions)

    json_object = json.dumps(final_questions)

# Save JSON Files

    with open("jsons/{}.json".format(txtFile.stem), mode='w') as file:

        file.write(json_object)
        file.close

# ---------------------------------------------------------------------------------------------------------------------- #
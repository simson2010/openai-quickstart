# Install Flask using pip if you haven't already
# pip install flask

from flask import Flask, render_template, request, redirect, url_for
from ai_translator.PdfTranslateHelper import PdfTranslateHelper
import uuid
import os

from dotenv import load_dotenv,find_dotenv  # Import load_dotenv
  # Load environment variables from .env
load_dotenv(find_dotenv())

app = Flask(__name__)
app.static_folder = 'static'  # Set the static folder
# Access the root path
root_path = app.root_path

pdf_temp_folder = 'pdf_temp'

# Rendering the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_language = request.form['from_language']
        to_language = request.form['to_language']
        
        pdf_file = request.files['pdf_file']
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            # Here, you would call your translation service with the PDF and language info
            # Translation code goes here
            config={
                "model_name":os.getenv("model_name"),
                "openai_key":os.getenv("openai_api_key")
                }
            translateHelper = PdfTranslateHelper(config=config)
            # Read PDF data;
            pdf_data = pdf_file.read()  # Read the PDF binary data
            # Save PDF file to temp folder
            # Generate a unique filename using UUID
            savedFileName = _saveTempFile(pdfData=pdf_data, origin_pdf_file=pdf_file)

            outfile = translateHelper.translate(root_path, savedFileName, from_language, to_language)
            print(f'output file {outfile}')
            # For now, let's just print the selected options
            print(f'saved file name {savedFileName}')
            print('From Language:', from_language)
            print('To Language:', to_language)
        else: 
            return render_template('fileformatincorrect.html')
        
    return render_template('index.html')


def _saveTempFile(pdfData, origin_pdf_file):
    unique_filename = f'{str(uuid.uuid4())}_{os.path.splitext(origin_pdf_file.filename)[0]}.pdf'
    pdf_filename = os.path.join(pdf_temp_folder, unique_filename)
    with open(pdf_filename, 'wb') as pdf_output:
        pdf_output.write(pdfData)
    return pdf_filename


if __name__ == '__main__':
    app.run(debug=True)



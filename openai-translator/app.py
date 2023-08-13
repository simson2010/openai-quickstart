# Install Flask using pip if you haven't already
# pip install flask

from flask import Flask, render_template, request, redirect, url_for, jsonify
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

template_error='fileformatincorrect.html'
template_index='index.html'
default_extension='.pdf'

param_from_lang="from_language"
param_to_lang="to_language"
param_pdf_file='pdf_file'

process_status_success=200
process_status_failed=400
# Rendering the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    output_book = None
    status = None
    if request.method == 'POST':
        from_language = request.form[param_from_lang]
        to_language = request.form[param_to_lang]
        
        pdf_file = request.files[param_pdf_file]
        if pdf_file and pdf_file.filename.endswith(default_extension):
            output_book = _handlePost(request, pdf_file, from_language, to_language)
        else: 
            return render_template(template_error)
    status = True if output_book else False
        
    return render_template(template_index, link=output_book, status = status)

# Run as web service
@app.route('/translate', methods=['POST'])
def translate():
    processed_data: dict = {"status":process_status_success, "file":""}
    if request.method == 'POST':
        from_language = request.form[param_from_lang]
        to_language = request.form[param_to_lang]
        
        pdf_file = request.files[param_pdf_file]
        if pdf_file and pdf_file.filename.endswith(default_extension):
            translatedbook = _handlePost(request, pdf_file, from_language, to_language)
            processed_data["file"] = translatedbook
        else: 
            processed_data["status"] = process_status_failed
            processed_data["error"] = "File format incorrect, please provide a valid PDF file instead."

    return jsonify(processed_data)

def _handlePost(request, pdf_file, from_lang, to_lang):
    # Here, you would call your translation service with the PDF and language info
    # Translation code goes here
    config={
        "model_name":os.getenv("model_name"),
        "openai_key":os.getenv("openai_api_key")
        }
    translateHelper = PdfTranslateHelper(config=config)
    translateHelper.current_host = request.host
    translateHelper.current_port = request.environ.get('SERVER_PORT')
    translateHelper.current_scheme = request.scheme
    # Read PDF data;
    pdf_data = pdf_file.read()  # Read the PDF binary data
    # Save PDF file to temp folder
    # Generate a unique filename using UUID
    savedFileName = _saveTempFile(pdfData=pdf_data, origin_pdf_file=pdf_file)

    outfile = translateHelper.translate(root_path, savedFileName, from_lang, to_lang)
    print(f'output file {outfile}')
    # For now, let's just print the selected options
    print(f'saved file name {savedFileName}')
    print('From Language:', from_lang)
    print('To Language:', to_lang)
    return outfile

def _saveTempFile(pdfData, origin_pdf_file):
    unique_filename = f'{str(uuid.uuid4())}_{os.path.splitext(origin_pdf_file.filename)[0]}{default_extension}'
    pdf_filename = os.path.join(pdf_temp_folder, unique_filename)
    with open(pdf_filename, 'wb') as pdf_output:
        pdf_output.write(pdfData)
    return pdf_filename


if __name__ == '__main__':
    app.run(debug=True)



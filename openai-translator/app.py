# Install Flask using pip if you haven't already
# pip install flask

from flask import Flask, render_template, request
import os

app = Flask(__name__)

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
            
            # For now, let's just print the selected options
            print(pdf_file)
            print('From Language:', from_language)
            print('To Language:', to_language)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

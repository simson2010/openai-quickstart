from ai_translator.utils import ArgumentParser, ConfigLoader, LOG
from ai_translator.model import GLMModel, OpenAIModel
from ai_translator.translator import PDFTranslator
import uuid

class PdfTranslateHelper:

    model_name: str = 'gpt-3.5-turbo'
    openai_api_key: str = None

    current_scheme: str = None
    current_host: str = None
    current_port: str = None
    
    def __init__(self, config: dict):
        print('init Helper')
        
        """init PdfTranslateHelper with uploaded PDF file name, from and to languages."""
        # Read environment variables
        print(config)
        self.model_name = config['model_name']
        self.openai_api_key = config['openai_key']


    def translate(self, root_path:str, pdf_name:str, from_lang:str, to_lang:str): 
        """Translate the PDF file to 'to_lang' and save to file, then return file name"""
        print(f'using model = {self.model_name} key={self.openai_api_key}')
        print(f'file: {pdf_name}, from {from_lang} to {to_lang}')

        # create model object for translate
        model = OpenAIModel(model=self.model_name, api_key=self.openai_api_key)

        translator = PDFTranslator(model)
        
        outFilePath = f'/static/pdfs/{str(uuid.uuid4())}_resultbook.pdf'

        diskFilePath = f'{root_path}{outFilePath}'

        httpDownloadPath = f'{self.current_scheme}://{self.current_host}{outFilePath}'

        translator.translate_pdf(pdf_file_path=pdf_name, target_language=to_lang, output_file_path=diskFilePath)

        return httpDownloadPath
    

    def _saveTranslatedBook():
        return ""
    

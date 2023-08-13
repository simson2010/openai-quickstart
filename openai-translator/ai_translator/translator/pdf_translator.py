from typing import Optional
from ai_translator.model import Model
from ai_translator.book import Book, Page, Content, ContentType, TableContent
from ai_translator.translator.pdf_parser import PDFParser
from ai_translator.translator.writer import Writer
from ai_translator.utils import LOG

class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self, pdf_file_path: str, file_format: str = 'PDF', target_language: str = '中文', output_file_path: str = None, pages: Optional[int] = None):
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                if content.content_type == ContentType.TEXT and content.original.strip() == '':
                    self.book.pages[page_idx].contents[content_idx].set_translation("  ", True)
                    continue
                prompt = self.model.translate_prompt(content, target_language)
                LOG.debug(prompt)
                sys_prompt=''
                if content.content_type == ContentType.TABLE:
                    sys_prompt = self.model.make_table_sys_prompt(target_language)
                if content.content_type == ContentType.TEXT:
                    sys_prompt = self.model.make_text_sys_prompt(target_language)
                # not to call when content_type is IMAGE
                if content.content_type != ContentType.IMAGE:
                    translation, status = self.model.make_request(prompt, sys_prompt=sys_prompt)
                LOG.info(translation)
                
                # handle image type 
                if content.content_type == ContentType.IMAGE:
                    status = True
                    translation = content.original
                    self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)
                    continue
                # Update the content in self.book.pages directly
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        self.writer.save_translated_book(self.book, output_file_path, file_format)

import pdfplumber
from typing import Optional
from ai_translator.book import Book, Page, Content, ContentType, TableContent
from ai_translator.translator.exceptions import PageOutOfRangeException
from ai_translator.utils import LOG
from PIL import Image


class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        book = Book(pdf_file_path)

        with pdfplumber.open(pdf_file_path) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                page = Page()

                # Store the original text content
                raw_text = pdf_page.extract_text(layout=True)
                tables = pdf_page.extract_tables()
                images = pdf_page.images

                LOG.debug(f"[parse_pdf | raw_text]\n\n {raw_text}")

                # Remove each cell's content from the original text
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            LOG.debug(f"[parse_pdf | cell]\n\n {cell}")
                            if cell is not None:
                                raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    newTextArr = []
                    tempString = '' 
                    for eachRawText in raw_text_lines:
                        is_blank = True if eachRawText.strip() == '' else False
                        #print(f'text = {eachRawText}, is_blank = {is_blank}')
                        if not is_blank:
                            tempString += eachRawText
                        if is_blank and tempString != '':
                            # trip tempString leading and trailing whitespaces
                            tempString = ' '.join(tempString.strip().split())
                            newTextArr.append(tempString)
                            newTextArr.append('  ')
                            newTextArr.append('  ')
                            tempString = ''

                    for eachRawText in newTextArr:
                        text_content = Content(content_type=ContentType.TEXT, is_title=False, original=eachRawText)
                        page.add_content(text_content)
                    
                    LOG.debug(f"[parse_pdf | raw_text]\n\n {cleaned_raw_text}")



                # Handling tables
                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")

                # handling images
                if images:  
                    for image in images:
                        bbox = (image["x0"], image["top"], image["x1"], image["bottom"])
                        cropped_page = pdf_page.crop(bbox)
                        img = cropped_page.to_image(antialias=True)

                        # Convert to PIL image
                        pil_image = img.original
                        image_content = Content(content_type=ContentType.IMAGE, is_title=False, original=pil_image)
                        page.add_content(image_content)
                        LOG.debug(f"[image]\n{image}")

                book.add_page(page)

        return book

from ai_translator.book import ContentType

class Model:
    def make_text_sys_prompt(self, target_language: str) -> str:
        return f"""
        Translate input text into {target_language}, keep spacing(spaces, separators, line breaks),
        only reply translated text. If no text to translate, reply nothing, empty string is fine."""
    
    def make_text_prompt(self, text: str, target_language: str) -> str:
        return f"""
        Translate below text into {target_language}:
        {text}"""

    def make_table_sys_prompt(self, target_language: str) -> str:
        return f'''
            Translate into {target_language}, keep spacing(spaces, separators, line breaks):
            1.Keep floating point in pricing value as is.
            2.Your should translate all single word or sentence in input text.
            3.Only feed me back the translated result.
            4.Remove all '[',']' in result, and separate each row with '||' and separate each column with ','.
            
            Sample 1 (English to Chinese):
            input English: [Fruit, Color, Price(USD)] [Apple, Red, 2.20] [Banana, Yellow, 1.50]
            output Chinese: 水果, 颜色, 价格(美元)||苹果, 红色, 2.20||香蕉, 黄色, 1.50

            Sample 2 (English to German):
            input English: [Fruit, Color, Price(USD)] [Apple, Red, 2.20] [Banana, Yellow, 1.50]
            output German: Frucht, Farbe, Preis (USD)||Apfel, Rot, 2.20||Banane, Gelb, 1.50
            '''
    
    def make_table_prompt(self, table: str, target_language: str) -> str:
        return f'''
            Translate below into {target_language}, only feed the result only:
            
            {table}'''

    def translate_prompt(self, content, target_language: str) -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, target_language)
        elif content.content_type == ContentType.TABLE:
            return self.make_table_prompt(content.get_original_as_str(), target_language)

    def make_request(self, prompt, **kwargs):
        raise NotImplementedError("子类必须实现 make_request 方法")

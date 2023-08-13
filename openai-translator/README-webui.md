<p align="center">
    <br> English | <a href="README-webui-CN.md">中文</a>
</p>

## PDF Translator

### Features
  - Select origin language
  - Select target langauge to be translated.
  - Upload your PDF file.
  - Translate PDF text to target language and save to new PDF file for download.
  - Keep PDF Table in document strucutre 
  - Keep Images in document structure. 
  - Provide WebService to translate PDF and return dowload URL.

### How to

#### Clone project. 

        ```shell
        git clone https://github.com/simson2010/openai-quickstart.git
        cd openai-quickstart
        git checkout feature/enhance_translator_2_0
        ```

#### Setup virtual env and install requirements.
       
        run below command in your termial. open your termail and chang dir to your local repo root folder

        ```shell
        $> python -m venv .venv 
        $> source ./.venv/bin/activate
        $> python -m pip install -r requirements.txt
        ```

#### Configue your OpenAI API Key and Model

        update your model and OpenAI API key in `.env` file in this repo root.

        ```shell
        model_name=gpt-3.5-turbo
        openai_api_key=your_key
        ``` 

#### Run Flask app

        ```shell
        $> python app.py
        ```
        then open http://127.0.0.1:5000 to enjoy yourself.

### Access via WebService

        You can access PDF translator via WebSerivce. You should pass below parameters to API: 

        - from_language: Origin language.
        - to_language: Target language to be translat to.
        - pdf_file: A path to your PDF file, to be upload to service. 

##### Response: 

            - "file": Translated content would be saved to a new PDF file for download.
            - "status": Transalte status, 
            - 200: success 
            - 400: failed
            - "error": Error message returned when status is 400.

##### Success Request:
        ```shell
        $> curl -X POST -F "from_language=English" -F "to_language=German" -F "pdf_file=@test.pdf" http://127.0.0.1:5000/translate

        ```

##### Response

            ```JSON
            {
            "file": "http://127.0.0.1:5000/static/pdfs/021986ac-c519-4a6c-b885-31845219f6ca_resultbook.pdf",
            "status": 200
            }
            ```

##### Failed Request

            ```shell
            $> curl -X POST -F "from_language=English" -F "to_language=German" -F "pdf_file=@test.csv" http://127.0.0.1:5000/translate

            ```

##### Response:

            ```JSON
            {
            "error": "File format incorrect, please provide a valid PDF file instead.",
            "file": "",
            "status": 400
            }
            ``` 

<p align="center">
    <br> <a href='./README-webui.md'>English</a> | 中文
</p>

## PDF翻译器

### 功能
- 选择源语言
- 选择要翻译成的目标语言。
- 上传你的PDF文件。
- 将PDF文本翻译成目标语言,保存成新的PDF文件供下载。
- 将PDF表格保留在文档结构中
- 将图像保留在文档结构中。
- 提供Web服务来翻译PDF并返回下载URL。

### 操作方法

#### 克隆项目。
 
    ```shell
    git clone https://github.com/simson2010/openai-quickstart.git
    cd openai-quickstart
    git checkout feature/enhance_translator_2_0
    ```
#### 设置虚拟环境并安装依赖。

    在终端运行以下命令。打开终端并将目录更改为本地仓库根目录

    ```shell
    $> python -m venv .venv
    $> source ./.venv/bin/activate  
    $> python -m pip install -r requirements.txt
    
    ```
#### 配置OpenAI API密钥和模型名字

    在此仓库根目录的`.env`文件中更新你的模型和OpenAI API密钥。

    ```shell
    model_name=gpt-3.5-turbo
    openai_api_key=你的密钥
    ```
#### 运行Flask应用

    ```shell
    $> python app.py
    ```
    然后打开http://127.0.0.1:5000享受功能。

### 通过Web服务访问

    您可以通过Web服务访问PDF翻译器。您应该向API传递以下参数:

    - from_language:源语言。
    - to_language:目标要翻译成的语言。
    - pdf_file:您的PDF文件路径,将上传到服务。

#### Web服务请求

### 响应:

        - "file": 翻译后的内容将保存成新的PDF文件供下载。
        - "status": 翻译状态,
        - 200: 成功
        - 400: 失败
        - "error": 当状态为400时返回的错误消息。

##### 成功请求
    ```shell
    $> curl -X POST -F "from_language=English" -F "to_language=German" -F "pdf_file=@test.pdf" http://127.0.0.1:5000/translate
    ```

##### 成功响应

        ```json
        {
        "file": "http://127.0.0.1:5000/static/pdfs/021986ac-c519-4a6c-b885-31845219f6ca_resultbook.pdf", 
        "status": 200
        }
        ```

##### 失败请求

        ```shell
        $> curl -X POST -F "from_language=English" -F "to_language=German" -F "pdf_file=@test.csv" http://127.0.0.1:5000/translate
        ```

##### 失败响应:

        ```json
        {
        "error": "文件格式不正确,请提供有效的PDF文件。",
        "file": "",
        "status": 400
        }
        ```
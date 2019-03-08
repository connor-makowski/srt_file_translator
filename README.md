SRT Translator
==========
A Python based Google Translate tool for SRT files.

Features
--------

- Easily translate SRT Files from English to any other language.
- Make batch translations into multiple languages.

Prerequisites
-------------

This project uses some open source projects to function:

* Google Translate - A simple translation API for python

How to Use
----------

Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Instructions

1. Clone this repo in your preferred directory and enter the repo:
    ```sh
    git clone https://github.com/connor-makowski/srt-translator.git
    cd srt-translator
    ```
2. Setup a virtual environment and install all requirements:
    ```
    python3 -m virtualenv venv
    ```
    Activate your virtual environment on Unix (Mac or Linux):
    ```
    source venv/bin/activate
    ```
    Activate your virtual environment on Windows:
    ```
    venv\Scripts\activate
    ```
    Install all requirements:
    ```
    pip install -r requirements.txt
    ```
3. Copy your Google-API Key over to the `google_key` folder in the root directory.
  - You can create a new json key [here](https://console.cloud.google.com/apis/credentials/serviceaccountkey).

4. Drop your current SRT files into the folder titled `inputs`.

5. Edit the `translator_options.py` file to match your needs.
    To see all languages, run:
    ```
    python see_languages.py
    ```

6. Use python to run the file `run.py`.
  ```
  python run.py
  ```

License
-------

Copyright 2018 Connor Makowski

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

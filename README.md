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

* [Google Translate] - A simple translation API for python

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
    ```sh
    python3 -m virtualenv venv
    ```
    Activate your virtual environment on Unix (Mac or Linux):
    ```sh
    source venv/bin/activate
    ```
    Activate your virtual environment on Windows:
    ```sh
    venv\Scripts\activate
    ```
    Install all requirements:
    ```sh
    pip install -r requirements.txt
    ```

3. Drop your current SRT files into the folder titled `inputs`.

4. Edit the `translator_options.py` file to match your needs.
    To see all languages, run:
    ```sh
    python see_languages.py
    ```

5. Use python to run the file `run.py`.
  ```sh
  python run.py
  ```

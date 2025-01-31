"""

# SRT File translator
[![PyPI version](https://badge.fury.io/py/srt_file_translator.svg)](https://badge.fury.io/py/srt_file_translator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An SRT translator for Python using Google Translate. This package breaks down given SRT formatted text into individual statments that are translated individually. Multi statement lines are broken down into single statement lines and statements that span multiple lines are aggregated into a single line. This allows google translate to translate each statement as a single unit and allows reasonable similarities to the original timing of the SRT file.

# Setup

Make sure you have Python 3.10.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Installation

```
pip install srt_file_translator
```

# Getting Started

`srt_file_translator` contains a basic `Translator` wrapper class that allows for easy translations of srt files. [Technical Docs Here](https://connor-makowski.github.io/srt_file_translator/srt_file_translator.html).

You need a Google Cloud API Key to use this library. You can create a new json key [here](https://console.cloud.google.com/apis/credentials/serviceaccountkey). Additonal information on how to get started using google cloud translate can be found [here](https://cloud.google.com/translate/docs/setup).

# Usage

## Translator Usage:
```py
# Import the Translator class
from srt_file_translator import Translator

# Initialize a translator object
translator = Translator(key_path="bq_key.json")

# Translate an srt file
translator.srt_file_translator(
    # The path to the srt file you want to translate
    source_file="test/myscript-en.srt",
    # The path to the output file
    target_file="test/myscript-es.srt",
    # The source language of the srt file
    source_language="en",
    # The target language of the output srt file
    target_language="es"
    # Optionally: Specify end of statement delimiter characters
    # for aggregating multi line statements into a single line
    statement_delimiters=['.', '?', '!']
    # Defaults to ['.', '?', '!']
)
```

## Show Available Languages:
```py
from srt_file_translator import Translator
translator = Translator(key_path="bq_key.json")
translator.show_languages()
```

## Actual Example:

Consider the following srt file:

```srt
0
00:00:00,000 --> 00:00:00,500


1
00:00:00,500 --> 00:00:04,620
Welcome to an introduction on how to use

2
00:00:04,620 --> 00:00:06,600
the Translate SRT package.

3
00:00:06,600 --> 00:00:08,540
This is only an example SRT

4
00:00:08,540 --> 00:00:12,130
file for the purpose of this demonstration.

```

Using the following code:
  
```py
from srt_file_translator import Translator
translator = Translator(key_path="bq_key.json")
translator.srt_file_translator(
    source_file="example_data/welcome_example-en.srt",
    target_file="example_data/welcome_example-es.srt",
    source_language="en",
    target_language="es"
)
```

Produces:

```srt
0
00:00:00,500 --> 00:00:06,600
Bienvenido a una introducción sobre cómo utilizar el paquete Translate SRT.

1
00:00:06,600 --> 00:00:12,130
Este es sólo un ejemplo de SRT.
```

Notice how the statements are aggregated into a single line before being translated. This allows google translate to translate the entire statement as a single unit. This is important because google translate will often translate individual words incorrectly if they are not in the context of an entire statement.

## Additional Examples:

### Translating all files in a folder to multiple languages:

```py
# Import the Translator class
from srt_file_translator import Translator
# Import os for file system operations
import os

# Initialize a translator object
translator = Translator(key_path="bq_key.json")

# Specify the input and output folders
input_folder = "example_data"
output_folder = "example_output"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Specify the source language and target languages
source_language = "en"
target_languates = ["es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko"]

# Loop through all files in the input folder
for file in os.listdir(input_folder):
    # Loop through all target languages
    for target_language in target_languates:
        # Translate each input file to each target language
        translator.srt_file_translator(
            source_file=os.path.join(input_folder, file),
            target_file=os.path.join(output_folder, f"{os.path.splitext(file)[0]}-{target_language}.srt"),
            source_language=source_language,
            target_language=target_language
        )
```


# License

Copyright 2024 Connor Makowski

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from .translator import Translator, SRT_Utils

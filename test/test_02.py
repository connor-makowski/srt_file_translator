from srt_file_translator import Translator
import os

translator = Translator(key_path="bq_key.json")

input_folder = "example_data"
output_folder = "example_output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

source_language = "en"
target_languates = ["es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko"]

for file in os.listdir(input_folder):
    for target_language in target_languates:
        source_file = os.path.join(input_folder, file)
        target_file = os.path.join(output_folder, f"{os.path.splitext(file)[0]}-{target_language}.srt")
        translator.srt_file_translator(
            source_file=source_file,
            target_file=target_file,
            source_language=source_language,
            target_language=target_language
        )


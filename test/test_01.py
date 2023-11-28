from srt_file_translator import Translator

translator = Translator(key_path="bq_key.json")

translator.srt_file_translator(
    source_file="example_data/welcome_example-en.srt",
    target_file="example_data/welcome_example-es.srt",
    source_language="en",
    target_language="es"
)
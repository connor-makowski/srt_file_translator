from srt_translator import Translator

translator = Translator(key_path="bq_key.json")

translator.translate_srt(
    source_file="test/W1L1_V01-en.srt",
    target_file="test/W1L1_V01-es.srt",
    source_language="en",
    target_language="es"
)
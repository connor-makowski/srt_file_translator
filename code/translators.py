from google.cloud import translate

def GoogleTranslate(input_text, out_language, in_language='en'):
    translate_client = translate.Client()
    translation = translate_client.translate(input_text, target_language=out_language)
    return translation

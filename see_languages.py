from google.cloud import translate

"""Code Below From Google"""

"""Lists all available languages."""
translate_client = translate.Client()

results = translate_client.get_languages()

for language in results:
    print(u'{name} ({language})'.format(**language))

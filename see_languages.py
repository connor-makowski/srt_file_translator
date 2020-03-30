from google.cloud import translate
from code.helpers import get_key_path
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
key_path = get_key_path(dir_path=dir_path)
translate_client = translate.Client.from_service_account_json(key_path)
results = translate_client.get_languages()

for language in results:
    print(u'{name} ({language})'.format(**language))

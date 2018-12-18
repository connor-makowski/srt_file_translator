from helpers import AggregateSentences, get_data_in_srt_format
from translators import GoogleTranslate
import codecs

def Translate(input_filepath, output_filepath, in_language, out_language):
    with codecs.open(output_filepath, "w+", encoding='utf-8-sig') as out_file:
        with open(input_filepath) as in_file:
            aggregate_sentences_dict=AggregateSentences(in_file)
            translations=GoogleTranslate(input_text=aggregate_sentences_dict['Text'], out_language=out_language, in_language=in_language)
            srt_file_format=get_data_in_srt_format(aggregate_sentences_dict, translations)
            for item in srt_file_format:
                out_file.write(item)

import os
import codecs
from google.cloud import translate

# Specify input and output Folder
input_folder="inputs"
output_folder="outputs"

# Get All Files in input Folder
dir_path = os.path.dirname(os.path.realpath(__file__))
all_files=os.listdir(dir_path + "/" + input_folder)



def Translate(filepath, out_language, in_language='en', file_end='.srt'):
    translate_client = translate.Client()
    with codecs.open(filepath+out_language+file_end, "w+", encoding='utf-8-sig') as out_file:
        with open(filepath+file_end) as myfile:
            for line in myfile:
                if line[0].isalpha():
                    translation = translate_client.translate(line, target_language=out_language)
                    out_file.write(translation['translatedText'])
                else:
                    print (line)
                    out_file.write(line)

x=Translate(r"./W1L1_V01-en", "zh-CN")

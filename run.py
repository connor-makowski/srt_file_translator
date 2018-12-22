import os
from translator_options import *
from code.translate import Translate

# Specify input and output Folder
input_folder="inputs"
output_folder="outputs"

# Get All Files in input Folder
dir_path = os.path.dirname(os.path.realpath(__file__))
all_files=os.listdir(dir_path + "/" + input_folder)

# Determine which files to translate
if translate_all_files:
    file_list=all_files
else:
    file_list=set(all_files).intersection(specific_files)

# Translate all files in file_list
for each_file in file_list:
    file_to_translate=dir_path + "/" + input_folder + "/" + each_file
    for each_language in output_languages:
        output_filename=each_file[:each_file.find('.srt')]+'-'+each_language+'.srt'
        file_to_output=dir_path + "/" + output_folder + "/" + output_filename
        results=Translate(input_filepath=file_to_translate,
        output_filepath=file_to_output, in_language=input_language, out_language=each_language)
        # print (results)

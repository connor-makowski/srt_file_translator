# Define a Function to get the key path for Google
def get_key_path(dir_path, key_location='google_key'):
    import os
    key_directory=dir_path+'/'+key_location
    key_file = [i for i in os.listdir(key_directory) if '__init__.py' not in i][0]
    key_path = key_directory+'/'+key_file
    return key_path

def AggregateSentences(in_file):
    import re
    time_structure=re.compile('\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')
    data={'Times':[],'Text':[]}
    use_next=False
    end_of_sentence=['.','?','!']
    endings=[0]
    for line in in_file:
        if time_structure.match(line[:-1]) is not None:
            data['Times'].append(line[:-1])
            use_next=True
        elif use_next:
            data['Text'].append(line[:-1])
            use_next=False
    for i in range(0,len(data['Text'])):
        if any(c in data['Text'][i] for c in end_of_sentence):
            endings.append(i)
    new_data={'Times':[],'Text':[]}
    is_break=False
    for i in range(1,len(endings)):
        start=endings[i-1]
        end=endings[i]
        if is_break:
            new_text=break_text
            is_break=False
        else:
            new_text=''
        for j in range(start+1,end+1):
            text_to_add=data['Text'][j]
            if j==end:
                index_location=max(text_to_add.rfind('?'),text_to_add.rfind('!'),text_to_add.rfind('.'))
                newer_text=text_to_add[:index_location+1]
                if index_location+1<len(text_to_add):
                    is_break=True
                    break_text=text_to_add[index_location+1:]
            else:
                newer_text=text_to_add
            new_text=new_text+" "+newer_text
        new_time=data['Times'][start][:12]+data['Times'][end][12:]
        new_data['Times'].append(new_time)
        new_data['Text'].append(new_text)
    return new_data

def get_data_in_srt_format(aggregate_sentences_dict, translations):
    times=aggregate_sentences_dict['Times']
    data=[]
    for i in range(0,len(times)):
        data.append(str(i) +'\n')
        data.append(times[i]+'\n')
        data.append(translations[i]['translatedText']+'\n')
        data.append('\n')
    return(data)

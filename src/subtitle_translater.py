from fnmatch import translate
from hashlib import new
import srt 
from googletrans import Translator
import numpy as np
import argparse


TARGET_LANGUAGE = "ta"
SOURCE_LANGUAGE = "en"

TARGET_LANGUAGE = "ta"
SOURCE_LANGUAGE = "en"



parser = argparse.ArgumentParser(description="""translate a .srt file using the free google translate api
you can change the target and source languages from the .py file """)
parser.add_argument("-i","--input", type=str, metavar="", required=True, help='the source file PATH')
parser.add_argument("-o","--output", type=str, metavar="", required=True, help='the translated file PATH')
args = parser.parse_args()



sub = open(args.input, "r")

org_sub_list = list(srt.parse(sub, "ignore_errors"))



translator = Translator()

src_text_list = []
dest_text_list = []
i = 0
for subtitle  in org_sub_list:
    i += 1
    text_to_translate = subtitle.content.replace("\n", " ")
    
    src_text_list.append(text_to_translate)

### trying to make translation faster and trick google api
pieces = 23
new_arrays = np.array_split(src_text_list, pieces)





joint_text_list = []
for item in new_arrays:
    joint_text_list.append("\n".join(item.tolist()))



joint_translated_list = translator.translate(joint_text_list, src=SOURCE_LANGUAGE,dest=TARGET_LANGUAGE)

translated_sub_list_list = []
for item in joint_translated_list:
    text_of_item = item.text
    translated_sub_list_list.append(text_of_item.split("\n"))

translated_sub_list = []
for i in translated_sub_list_list:
    for j in i:
        translated_sub_list.append(j)

print(str(len(translated_sub_list)) + "==" + str(len(org_sub_list)) + "  <-- these two numbers need to be the same.")




for translation,srt_object in zip(translated_sub_list ,org_sub_list):

    srt_object.content = translation



new_sub = open(args.output,"w", encoding="utf-8")

new_sub.write(srt.compose(org_sub_list))


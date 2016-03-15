# -*- coding: utf-8 -*-

#import subprocess
import os
import string
import re


def extract_text(): # извлекает текст из xml
    os.system("python3 WikiExtractor.py --infn /Users/anastasiaromanova/Desktop/mine/Programming/WikiExtractor/mdfwiki-20160305-pages-meta-current.xml.bz2")
    return
    
#def extract_text_1(): # тоже извлекает текст из xml. можно использовать вместо os.system   
#    subprocess.call([
#                'python3',
#                'WikiExtractor.py',
#                '--infn',
#                '/Users/anastasiaromanova/Desktop/mine/Programming/WikiExtractor/mdfwiki-20160305-pages-meta-current.xml.bz2',
#    ])
#    return

def count_words(text): #считает слова в тексте
    words = re.split(r"[ %s\t\n\-\—\–0123456789«»]+" % (string.punctuation,), text.lower())
    for word in words:
        if word in freq_list:
            freq_list[word] += 1
        else:
                freq_list[word] = 1
    return text
   
def sort_freq_list(freq_list): # сортирует частотный словарь по убыванию
    sorted_freq_list = sorted(freq_list.items(), key = lambda x:x[1], reverse = True)
    for word, freq in sorted_freq_list:
        frequency.write(word + "\t" + str(freq) + "\n")
#        print("%-10s %d" % (word, fr))
    return freq_list



extract_text()
print('Text from xml extracted')

with open("Wiki.txt", "r", encoding = "utf-8") as file: # открываем файл, вызываем функции
    frequency = open("freq.tsv", "w", encoding = "utf-8")
    freq_list = {}
    line = []
    text = file.read()
    count_words(text)
    sort_freq_list(freq_list)
    
    
file.close()
frequency.close()

print("Words' frequency counted" )
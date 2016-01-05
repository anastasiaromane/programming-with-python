# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:41:31 2015

@author: anastasiaromanova
# transliteration of Georgian texts to IPA
# function to transliterate
"""
original_poems = open("Original_Georgian_poems.txt", "r", encoding = "utf-8")
trans_poems = open("Transliterated_Georgian_poems.txt", "w", encoding = "utf-8")
name = original_poems.read()

def transliterate(name):
    dictionary = {'ა':'ɑ',
                  'ბ':'b', 
                  'გ':'g',
                  'დ':'d',
                  'ე':'ɛ',
                  'ვ':'v',
                  'ზ':'z',
                  'ჱ':'ɛj',
                  'თ':'tʰ',
                  'ი': 'ɪ',
                  'კ':'kʼ',
                  'ლ':'l',
                  'მ':'m',
                  'ნ':'n',
                  'ჲ':'j',
                  'ო':'ɔ',
                  'პ':'pʼ',
                  'ჟ':'ʒ',
                  'რ':'r',
                  'ს':'s',
                  'ტ':'tʼ',
                  'ჳ':'wi', 
                  'უ':'u',
                  'ფ':'pʰ',
                  'ქ':'kʰ',
                  'ღ':'ɣ',
                  'ყ': 'qʼ',
                  'შ': 'ʃ',
                  'ჩ':'tʃ',
                  'ც':'ts', 
                  'ძ':'dz',
                  'წ':'tsʼ',
                  'ჭ':'tʃʼ',
                  'ხ':'x',
                  'ჴ':'q',
                  'ჯ':'dʒ',
                  'ჰ':'h',
                  'ჵ':'hɔɛ'}
    
    
    for i in dictionary:
        name = name.replace(i,dictionary[i])
    return name
if __name__=="__main__":
    trans_poems.write(transliterate(name))

original_poems.close()
trans_poems.close()
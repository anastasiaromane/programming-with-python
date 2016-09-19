# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:41:31 2015

@author: anastasiaromanova
# transliteration - Amharskiy to Latin
# function to transliterate
"""

amhar_pismo = open("amhar_pismo.tsv", "r", encoding = "utf-8")

voc = []
cons = []
alph = {}

c = 0
for line in amhar_pismo:
    line = line.strip('\n')
    line = line.split('\t')
    v = 0 
    for symbol in line:
        if c == 0 and v != 0:
            voc.append(symbol)
        elif c != 0 and v == 0:
            cons.append(symbol)
        elif c != 0 and v != 0:
            alph[symbol] = cons[c-1] + voc[v-1]
        v += 1        
    c += 1

   
original = open("original.txt", "r", encoding = "utf-8")
final = open("final.txt", "w", encoding = "utf-8")                    
name = original.read()

def transliterate(name):
    dictionary = alph
    
    for i in dictionary:
        name = name.replace(i, dictionary[i])
    return name
if __name__=="__main__":
    final.write(transliterate(name))

amhar_pismo.close()
original.close()
final.close()
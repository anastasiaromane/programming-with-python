# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:32:26 2015

@author: anastasiaromanova
This is the Irish forms dictionary.
The dict looks like - form : lemma
"""
import re


f = open("irish.html", "r", encoding = "utf-8")
irish = f.read()

#searching for a lemma
lemma = re.search('<h3.*?>([^|]+)</h3>', irish).group(1)
irish_lemma = lemma.strip('\n ')

#searching for forms and creating a list of forms
n = re.search('<p.*?>Forms:([^|]+)<\/p.+">', irish).group(1)
n = n.strip('\n \t ')
forms_list = n.split(', ')

#creating a dictionary
irish_forms_dict = dict.fromkeys(forms_list, irish_lemma)

#putting the dict into a file.txt
irish_forms_dictionary = open("irish_forms_dictionary.txt", "w", encoding = "utf-8")
irish_forms_dictionary.write(str(irish_forms_dict)) 
#print(irish_forms_dict)

f.close()
irish_forms_dictionary.close()
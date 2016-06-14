#coding='utf-8'

import re
from lxml import etree

"""
Создаем файл с текстом по образцу:
Тэги: lex для лексемы, transcr для транскрипции, sem для значения.
"""
def make_file(data, s):
    one = ''
    char = ''
    for i in range(len(s)):
        if s[i] in "“ 。”，！‘…：？-、ａ； ":
                one += s[i]
                if char:
                    one += '<w>'
                    for d in data[char]:
                        one += '<ana lex="{}" transcr="{}" sem="{}"/>'.format(char, d[0], d[1])
                    
                    one += char + '</w>'
                    char = ''
        else:
            char += s[i]
            if data.get(char) is not None:
                continue
            else:
                char = char[:-1]
                one += '<w>'
                for d in data[char]:
                    one += '<ana lex="{}" transcr="{}" sem="{}"/>'.format(char, d[0], d[1])
                
                one += char + '</w>'
                char = ''
    #print('<se>' + one + '</se>', file=open('check_out.txt','w',encoding='utf-8'))
    return '<se>' + one + '</se>'

"""
Достаем из словаря слово на новокитайском, его транскрипцию и значение.
"""
def get_data():
    pattern = re.compile(r'\n.*? (.*?) \[(.*?)\] /(.*)/')
    chinese_dict = open('cedict_ts.u8', encoding='utf-8').read()
    data = {}
    for x in re.findall(pattern, chinese_dict):
        sem = ''.join([l.replace('/', ',') for l in x[2] if l not in '"&'])
        if data.get(x[0]) is not None:
            data[x[0]].append((x[1], sem))
        else:
            data[x[0]] = [(x[1],sem)]
    return data

def main():
    data = get_data()
    text = open('stal.xml', encoding='utf-8').read()
    text = etree.fromstring(text)
    sents = text.xpath('//se[not (@lang="ru")]')
    for s in sents:
        sub = etree.fromstring(make_file(data, s.text))
        s = s.getparent().replace(s, sub)
    etree.ElementTree(text).write('chinese_text.txt', encoding='utf-8', pretty_print=True)

if __name__ == '__main__':
    main()
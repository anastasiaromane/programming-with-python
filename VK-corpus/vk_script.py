# coding: utf-8

import csv
import requests

"""
Сначала создаем файл с метаданными нашего мини-корпуса.

Метаданные являются некоторой социолингвистической информацией о зарегестрированных 
в VK жителях города Ромоданово, Республика Мордовия.

Добавляем заголовки: ID, Last Name, First name, Sex, Birthday, Occupation,
Religion и Languages.

"""

def header(report):
    report.writerow(['ID','Last Name','First name','Sex','Birthday','Occupation',
                     'Religion', 'Languages'])

"""
Находим данные о пользователях, записываем в сsv-файл.

Скачиваем посты пользователей с их стены в VK в txt-файлы.

Если стена пустая, файл для этого пользователя не заводим.

"""
def get_data(report):
    main_method = 'https://api.vk.com/method/users.search'
    parameters = {
        'access_token':'5c932ca0c91dbd5ece6b581151e62eba57cc4d6f27d38afec60f1d3bc4e9adad8f40efdff576daa2b70f1',
        'count':500,
        'country': 1,
        'city': 1053008, 
        'fields':'bdate, last_name, first_name, sex, occupation, personal'
        }
    users = requests.get(main_method, params=parameters)
    
    data = users.json()

    for i in range(1, len(data['response'])):
        if data['response'][i]['sex'] is not None:
            if data['response'][i]['sex'] == 1:
                sex = 'female'
            else:
                sex = 'male'
        if data["response"][i].get('bdate')  is not None:
            birthday = data["response"][i].get("bdate")
            #print(birthday)
        if data['response'][i].get('occupation') is not None:
            uni = data['response'][i]['occupation']['name']
        if data['response'][i].get('occupation') is None:
            uni = ''
        if data['response'][i].get('personal') is not None:
#            print(data['response'][i].get('personal'))
            if type(data['response'][i].get('personal')) is dict:
                for key, value in data['response'][i].get('personal').items():
                    if key =='religion':                    
                        religion = value
                    if key == 'langs':
                        languages = value
                        #print(languages)
        if data['response'][i].get('personal') is  None:
            religion = ''
            languages = ''


        info = (data['response'][i]['uid'],data['response'][i]['last_name'],
                data['response'][i]['first_name'], sex, birthday, uni, religion,
                 ', '.join(languages))
        report.writerow(info)                
            
        user = data['response'][i]['uid']
        #posts_method = 'https://api.vk.com/method/wall.get'         
        get_posts = requests.get('https://api.vk.com/method/wall.get',
                                 params={'owner_id':user, 'count':100, 'filter':'owner'})
        wall_data = get_posts.json()

        try:
            for wall in wall_data['response'][1:]:
                wall['text'] = wall['text'].replace('<br>','\n')
                if len(wall['text']) > 1:
                    with open('Posts/wall_' + str(user) + '.txt', 'a', encoding='utf16') as f_out:
                        f_out.write(wall['text'] + '\n')
        except:
            pass

def main():
    report_file = open('vk_report.csv', 'w', encoding='utf16')
    report = csv.writer(
    report_file, delimiter="\t", quotechar='',
    quoting=csv.QUOTE_NONE
)
    header(report)
    get_data(report)
    
    
if __name__ == '__main__':
        main()             
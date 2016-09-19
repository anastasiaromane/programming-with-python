# -*- coding: utf-8 -*-

import pymysql
import csv

#вытаскиваем данные из файла csv и добавляем их в первую созданную таблицу, которая содержит ссылки на статьи
def get_data_one(file):
    links = []
    with open(file, "r", encoding='windows-1251') as f_in:
        reader = csv.reader(f_in, delimiter=";")
        for row in reader:
            links.append(row[1])
    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='pass_sql_word@',
                             db ='orenburg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            for link in links:
                table_two = "INSERT INTO `source` (`source`) VALUES (%s)"
                cursor.execute(table_two, (link))
        print('Links inserted')        
        conn.commit()
    finally:
        conn.close()
        print('Data inserted')        

#вытаскиваем данные из файла csv и добавляем их во вторую таблицу, которая содержит названия и авторов статей
def get_data_two(file):
    authors = []
    headers =[]
    with open(file, "r", encoding='windows-1251') as f_in:
        reader = csv.reader(f_in, delimiter=";")
        for row in reader:
            authors.append(row[1])
            headers.append(row[2])
#    print(headers[:3])
    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='pass_sql_word@',
                             db ='orenburg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            for author in authors:
                table_three = "INSERT INTO `title` (`author`) VALUES (%s)"
                cursor.execute(table_three, (author))
        print('Authors inserted')
        with conn.cursor() as cursor:
            for header in headers:
                table_four = "INSERT INTO `title` (`header`) VALUES (%s)"
                cursor.execute(table_four, (header))
        print('Headers inserted')        
        conn.commit()
    finally:
        conn.close()
        print('Data inserted')        
                
# создаем базу данных orenburg
def create_db():
    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='pass_sql_word@',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            db = 'CREATE DATABASE orenburg'
            cursor.execute(db)
        conn.commit()
        print('Orenburg created')
    finally:
        conn.close()

#создаем первую таблицу с ссылками на статьи
def create_table_one():
    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='pass_sql_word@',
                             db ='orenburg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            table_one = "CREATE TABLE `source` (`id` int(11) NOT NULL AUTO_INCREMENT, `source` varchar(255) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"
            cursor.execute(table_one)
        conn.commit()
    finally:
        conn.close()
        print('Table created')        

#создаем вторую таблицу с названийми и авторами статей    
def create_table_two():
    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='pass_sql_word@',
                             db ='orenburg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            table_two = "CREATE TABLE `title` (`id` int(11) NOT NULL AUTO_INCREMENT, `author` TEXT, `header` TEXT, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"
            cursor.execute(table_two)
        conn.commit()
    finally:
        conn.close()
        print('Table created')        


#функция для удаления таблиц 
def drop_table():
    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='pass_sql_word@',
                             db ='orenburg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS title")
        conn.commit()
    finally:
        conn.close()
        print('Table removed')  
        
#Используем таблицу
def use_db():
    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='pass_sql_word@',
                             db ='orenburg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            #sql = "SELECT `id`, `author` FROM `title` WHERE `header`=%s"
            sql = "SELECT title.*, source.* from title, source where title.id = source.id"
            #cursor.execute(sql, ('Изумрудный вальс',))
            #sql = "SHOW TABLES"
            cursor.execute(sql)
            result = cursor.fetchone()
        print(result)        
    finally:
        conn.close()
        
        
print('Creating Database Orenburg...')                         
create_db()
create_table_one()
create_table_two()
get_data_one("table_one.csv")
get_data_two("table_two.csv")
drop_table()
print('Database is ready to use')
        
print("Let's use database")
use_db()
print('Done')        
        
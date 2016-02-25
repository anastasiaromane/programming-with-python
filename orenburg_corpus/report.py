# -*- coding: utf-8 -*-

import csv
from datetime import date
from settings import REPORT_FILE


SPHERE = "публицистика"
TOPIC = ""
STYLE = "нейтральный"
AUDIENCE_AGE = "н-возраст"
AUDIENCE_LEVEL = "н-уровень"
AUDIENCE_SIZE = "городская"
MEDIUM = "газета"
COUNTRY = "Россия"
REGION = "Оренбург"
LANGUAGE = "ru"
PUBLICATION = "Вечерний Оренбург"

report_file = open(REPORT_FILE, 'a', newline='', encoding='windows-1251')

report = csv.writer(
    report_file, delimiter=";", quotechar='"',
    quoting=csv.QUOTE_ALL
)


def header():
    report.writerow([
        'path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere',
        'genre_fi', 'type', 'topic', 'chronotop', 'style', 'audience_age',
        'audience_level', 'audience_size', 'source', 'publication',
        'publisher', 'publ_year', 'medium', 'country', 'region', 'language',
    ])


def write(path, header, created, source, author=''):
    """ Пишет в файл отчёта строку с данными в кодировке windows-1251

    Args:
        path (unicode):  путь к файлу со статьёй
        header (unicode): название статьи
        created (datetime.date): дата публикации
        source (unicode): URL, откуда статья была скачана
        author (unicode): имя автора, если оно есть

    Returns:
        None

    """
    result = [
        path,
        author,
        "",
        "",
        header,
        date.strftime(created, "%d.%m.%Y"),
        SPHERE,
        "",
        "",
        "",
        "",
        STYLE,
        AUDIENCE_AGE,
        AUDIENCE_LEVEL,
        AUDIENCE_SIZE,
        source,
        PUBLICATION,
        "",
        created.year,
        MEDIUM,
        COUNTRY,
        REGION,
        LANGUAGE,
    ]

    report.writerow(result)
    report_file.flush()
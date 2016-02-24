# -*- coding: utf-8 -*-

import csv
from datetime import date
from settings import REPORT_FILE


class Report(object):
    """Формирование файла отчёта"""

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

    def __init__(self):
        self.report_file = open(REPORT_FILE, 'a', newline='', encoding='windows-1251')
        self.report = csv.writer(
            self.report_file, delimiter=";", quotechar='"',
            quoting=csv.QUOTE_ALL
        )

        # head
        self.report.writerow([
            'path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere',
            'genre_fi', 'type', 'topic', 'chronotop', 'style', 'audience_age',
            'audience_level', 'audience_size', 'source', 'publication',
            'publisher', 'publ_year', 'medium', 'country', 'region', 'language',
        ])

    def write(self, path, header, created, source, author=''):
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
            self.SPHERE,
            "",
            "",
            "",
            "",
            self.STYLE,
            self.AUDIENCE_AGE,
            self.AUDIENCE_LEVEL,
            self.AUDIENCE_SIZE,
            source,
            self.PUBLICATION,
            "",
            created.year,
            self.MEDIUM,
            self.COUNTRY,
            self.REGION,
            self.LANGUAGE,
        ]

        self.report.writerow(result)
        self.report_file.flush()

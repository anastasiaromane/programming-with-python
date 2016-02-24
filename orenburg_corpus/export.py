# -*- coding: utf-8 -*-

import os
import subprocess
import datetime
from pymystem3 import Mystem
from slugify import slugify
from settings import RESULT_DIR

mystem = Mystem()


def get_path(date, title, extension, version):
    """Возвращает путь до файла, в зависимости от входных данных.

    Args:
        date (datetime.date)
        title (str)
        extension (str): расширение файла без точки (txt, html, xml, etc.)
        version (Optional[str]): версия. К примеру: lemm_text, original_text

    Returns:
        str: /tmp/orenburg/2015/04/10042015_poliot-navstrechu-pobede_orig.txt

    """
    # без расширения для облегчённой обрезки
    filename = "%(day)d%(month)d%(year)d_%(title)s" % {
        'day': date.day,
        'month': date.month,
        'year': date.year,
        'title': slugify(title),
    }

    path = os.path.join(
        RESULT_DIR,
        str(date.year),
        str(date.month),
        version,
        filename
    )

    # длина пути в большинстве FS ограничена 255 символами. Наше имя файла
    # генерируется без расширения, чтобы было легче обрезать, в итоге
    # мы должны обрезать путь до файла до 255 символов минус количество
    # символов в расширении минус 1 (точка между именем файла и расширением)
    path = path[:255 - len(extension) - 1].strip('-')

    # добавляем расширение
    path = "%s.%s" % (path, extension)

    return path


def save(data, path):
    """ Сохраняет данные. При необходимости рекурсивно создаёт директории.

    Args:
        data (unicode): информация, которую следует сохранить
        path (unicode): абсолютный путь до файла

    Returns:
        None

    """
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(path, 'w', encoding='utf8') as f:
        f.write(data)


def get_original_text(text, title, date, url, author='', topic=''):
    """Приводим текст к нужному виду:

    @au имя автора (если автора нет, пишем Noname)
    @ti Название статьи
    @da дата в формате 12.02.2012
    @topic категория, если мы её можем найти на странице со статьёй
    @url URL, откуда мы скачали страницу

    ==Текст==

    Args:
        text (unicode)
        title (unicode)
        date (datetime.date)
        url (unicode): откуда мы скачали страницу
        author (Optional[unicode])
        topic (Optional[unicode]): категория

    Returns:
        str: текст в нужном виде

    """
    pre = ("@au %(author)s\n"
           "@ti %(title)s\n"
           "@da %(date)s\n"
           "@topic %(topic)s\n"
           "@url %(url)s")

    date = datetime.date.strftime(date, "%d.%m.%Y")
    pre = pre % {
        'author': author,
        'title': title,
        'date': date,
        'topic': topic,
        'author': author if author else 'Noname',
        'url': url,
    }

    return "%s\n\n%s" % (pre, text.strip())


def lemmatisation(input_file, output_file, output_format='text'):
    """Лемматизация и экспорт результата.

    Args:
        input_file (unicode): путь до файла с текстом, который нужно лемматизировать
        output_file (unicode): путь до файла с результатом лемматизации
        output_format (unicode): text, xml или json

    Returns:
        None

    """
    # для текстового формата используем pymystem3
    if output_format == 'text':
        with open(input_file, 'r') as fr:
            input_data = fr.read()

        with open(output_file, 'w') as fw:
            trash = set([' ', '\n', '.', '!', '?', ',', ':', ';'])
            lemmas = mystem.lemmatize(input_data)
            lemmas = [l for l in lemmas if (len(l.strip()) > 1 and
                                            not l.strip() in trash
                                            and l.strip().isalnum())]
            fw.write(' '.join(lemmas))

            return

    # для остальных форматов запускаем бинарник с необходимыми аргументами
    subprocess.call([
        mystem._mystem_bin,
        input_file,
        output_file,
        '-l',
        '--format',
        output_format
    ])

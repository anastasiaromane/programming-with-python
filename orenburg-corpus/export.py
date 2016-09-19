# -*- coding: utf-8 -*-

import os
import subprocess
import datetime
from pymystem3 import Mystem
from slugify import slugify
from settings import RESULT_DIR

mystem = Mystem()


def get_path(date, title, extension, version):#путь к файлу
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

    path = path[:255 - len(extension) - 1].strip('-')

    # добавляем расширение
    path = "%s.%s" % (path, extension)

    return path


def save(data, path):#для сохранения данных в директориях
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(path, 'w', encoding='utf8') as f:
        f.write(data)


def get_original_text(text, title, date, url, author='', topic=''):#добавляем теги в статьи (@au,@ti, @da, @topic, @url)
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


def lemmatisation(input_file, output_file, output_format='text'): #лемматизация
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

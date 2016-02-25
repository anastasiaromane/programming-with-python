# -*- coding: utf-8 -*-

import sys
from datetime import date
import requests
from lxml import html
from settings import ARCHIVE_LINK, VISITED_LINKS
from export import get_path, get_original_text, save, lemmatisation
import report


chars_counter = 0
visited_links_file = open(VISITED_LINKS, 'r+')
visited_links = list(map(str.strip, visited_links_file.readlines()))
report.header()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Accept-Encoding': 'deflate',
    'Accept-Language': 'en-US,en;q=0.5'
}



def str_to_date(string):
    m = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
         'августа', 'сентября', 'октября', 'ноября', 'декабря']

    # ['10', 'февраля', '2016']
    try:
        day, month, year = string.split(' ')[3:6]
        # номер месяца - это индекс + 1
        month = m.index(month) + 1
    except (IndexError, ValueError):
        return None

    return date(year=int(year), month=month, day=int(day))

xpathes = {
    'year_links': '//div[@class="news-year"]/a/@href',
    'archive_links': '//div[@class="clauses-arhive"]/a/@href',
    'list_news_links': '//div[@class="clauses-name"]/a/@href',
    'news_element': '//div[@class="clauses_text"]',
    'news_date': '//div[@class="number_current_id"]/a/text()',
    'news_anons': '//div[@class="clauses_anons"]/p',
}

# главная страница архива
archive = html.fromstring(requests.get(ARCHIVE_LINK, headers=headers).content)

# ссылки на список выпусков по годам
archive_links = []
for year_link in archive.xpath(xpathes['year_links']):
    year_archive_page = html.fromstring(requests.get(
        year_link,
        headers=headers
    ).content)
    archive_links += year_archive_page.xpath(xpathes['archive_links'])

# ссылки на новости
list_news_links = []
for archive_link in archive_links:
    list_news_page = html.fromstring(requests.get(
        archive_link,
        headers=headers
    ).content)
    list_news_links += list_news_page.xpath(xpathes['list_news_links'])

# обработка новостей
for news_link in list_news_links:
    if news_link in visited_links:
        continue

    raw_news_page = requests.get(news_link, headers=headers).content
    news_page = html.fromstring(raw_news_page)

    # сохраняем ссылку по которой перешли
    visited_links_file.write("%s\n" % news_link)

    try:
        news_element = news_page.xpath(xpathes['news_element'])[0]
    except IndexError:
        # если текста новости нет
        continue

    try:
        news_date = news_page.xpath(xpathes['news_date'])[0]
        news_date = str_to_date(news_date)

        if not news_date:
            continue
    except IndexError:
        # если даты нет
        continue

    # замена <br> на \n в тексте новости
    for br in news_element.xpath("*//br"):
        br.tail = "\n" + br.tail if br.tail else "\n"

    anons = news_page.xpath(xpathes['news_anons'])

    try:
        author = anons[0].text_content()
    except IndexError:
        author = ''

    # если в первом параграфе анонса содержится текст, то, зачастую, это
    # имя и фамилия автора. Однако, иногда это может быть и текст
    # анонса, поэтому считаем, что это имя и фамилия, только если первый
    # параграф состоит из двух слов
    if len(author.split(' ')) != 2:
        author = ''

    news_text = ""

    # начинаем новость с анонса
    for i in anons[1:]:
        news_text += i.text_content()
        news_text += "\n"

    news_text += news_element.text_content()
    news_text = news_text.strip()

    # новости без текста (скорее всего, фотоотчет) не нужны
    if not news_text:
        continue

    chars_counter += len(news_text)

    orig_path = get_path(news_date, title, 'txt', version='original_text')
    text_lemma_path = get_path(news_date, title, 'txt', version='lemm_text')
    xml_path = get_path(news_date, title, 'xml', version='xml')
    html_path = get_path(news_date, title, 'html', version='html')

    # сохраняем текст статьи, но пока без шапки, чтобы mystem не работал с
    # лишними данными
    save(news_text, orig_path)

    # необходимо для рекурсивного создания дирректорий, в ином случае данные
    # лемматизации некуда будет сохранять
    save('', text_lemma_path)
    save('', xml_path)

    lemmatisation(orig_path, xml_path, 'xml')
    lemmatisation(orig_path, text_lemma_path, 'text')

    # пересохраняем текст статьи уже с шапкой, т.к. лемматизация окончена
    text = get_original_text(news_text, title, news_date, news_link, author)
    save(text, orig_path)

    # сохранчем html страницу
    save(raw_news_page.decode('utf8'), html_path)

    # добавляем данные о новости в отчёт
    report.write(orig_path, title, news_date, news_link, author)



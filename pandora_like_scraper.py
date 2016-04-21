#!/usr/bin/python

from __future__ import print_function
from lxml import html
import sys
import json
import requests
import re

OUT_HTML = 'likes.html'
OUT_JSON = 'likes.json'
IN_TEMPLATE = 'template.html'
IN_COOKIES = 'cookies.txt'

GET_ROOT = 'http://www.pandora.com'
GET_LIKES = 'http://www.pandora.com/content/tracklikes?webname={username}&thumbStartIndex={index}'
GET_LIKES_CNT = 5   # number of likes returned per request


def scrape_user(username, save_html=True, save_json=True, max_recent=sys.maxint):
    """ Scrapes pandora likes from user """
    print('Scraping pandora likes from {}...'.format(username))

    cookies = load_cookies()

    likes = list()

    # Get all likes
    i = 0
    while i < max_recent:
        new = get_like_index(username, i, cookies)

        if len(new) == 0:
            break

        likes.extend(new)
        i += GET_LIKES_CNT

    # Remove excess
    while len(likes) > max_recent:
        likes.pop(len(likes)-1)

    # Remove duplicates
    for i in range(0, len(likes)):
        if i <= len(likes)-2:
            for j in range(i+1, len(likes)):
                if str(likes[i]) == str(likes[j]):
                    likes.pop(j)

    if save_html:
        save_json_file(likes)
    if save_json:
        save_html_file(username, likes)

    return likes


def load_cookies():
    cookies = dict()
    pattern = re.compile(r'([^=;]+)=([^=;]+);')

    fi = open(IN_COOKIES, 'r')
    cookie_str = fi.readline()
    fi.close()

    for (name, value) in re.findall(pattern, cookie_str):
        cookies[name] = value

    return cookies


def get_like_index(username, index, cookies):
    """ Pulls info from each song in the index """
    print('Grabbing index {}...'.format(index))

    page = requests.get(GET_LIKES.format(username=username, index=index), cookies=cookies)
    root = html.fromstring(page.text)

    def clean(result):
        if len(result) > 0:
            return result[0]
        else:
            return '?'

    likes = list()
    for info_box in root.xpath("//div[contains(@class, 'infobox i-t-shade-1')]"):
        like = dict()
        like['albumArt'] = clean(info_box.xpath(".//div[@class='infobox-thumb']/img/@src"))
        like['song'] = clean(info_box.xpath(".//div[@class='infobox-body']/h3/a/text()"))
        like['artist'] = clean(info_box.xpath(".//div[@class='infobox-body']/p[1]/a/text()"))

        song_page = requests.get(GET_ROOT + info_box.xpath(".//div[@class='infobox-body']/h3/a/@href")[0], cookies=cookies)
        song_root = html.fromstring(song_page.text)

        like['audioFile'] = clean(
            song_root.xpath("//div[contains(@class, 'backstage')]/meta[@itemprop='audio']/@content"))
        like['album'] = clean(song_root.xpath("//a[contains(@class, 'album_link')]/text()"))

        if like['album'] == '?':
            like['album'] = clean(song_root.xpath("//span[contains(@class, 'album_link')]/text()"))

        likes.append(like)

    return likes


def save_json_file(likes):
    data = dict()
    data['likes'] = likes

    fo = open(OUT_JSON, 'w')
    fo.write(json.dumps(data, indent=4))
    fo.close()


def save_html_file(username, likes):
    # Load template
    template = open(IN_TEMPLATE, 'r')
    in_html = ''.join(template.readlines())
    template.close()

    # Create headers
    headers = ''
    headers += '<th>Album Art</th>'
    headers += '<th>Artist</th>'
    headers += '<th>Album</th>'
    headers += '<th>Song</th>'
    headers += '<th>Audio File</th>'

    # Create rows
    rows = ''
    for like in likes:
        rows += '<tr>'
        rows += '<td><div class="album-art"><a href="{0}"><img src="{0}"/></a></div></td>'.format(like['albumArt'])
        rows += '<td>' + like['artist'] + '</td>'
        rows += '<td>' + like['album'] + '</td>'
        rows += '<td>' + like['song'] + '</td>'
        rows += '<td><a target="_blank" href="' + like['audioFile'] + '">Play</a></td>'
        rows += '</tr> '

    # Escape all brackets
    in_html = in_html.replace('{', '{{').replace('}', '}}')
    # Un-escape variable brackets
    in_html = in_html.replace('{{username}}', '{username}')
    in_html = in_html.replace('{{rows}}', '{rows}')
    in_html = in_html.replace('{{headers}}', '{headers}')
    in_html = in_html.format(username=username, rows=rows, headers=headers)

    # Save as html
    fo = open(OUT_HTML, 'w')
    fo.write(in_html)
    fo.close()


if __name__ == '__main__':
    argc = len(sys.argv)

    if argc <= 1:
        scrape_user(str(input('Enter the pandora user to scrape likes from: ')))
    else:
        scrape_user(
            sys.argv[1],
            (str(sys.argv[2]).lower() == 'true') if argc >= 3 else True,
            (str(sys.argv[3]).lower() == 'true') if argc >= 4 else True,
            int(sys.argv[4]) if argc >= 5 and str(sys.argv[4]).isdigit() else sys.maxint
        )


#!/usr/bin/python

from __future__ import print_function
from lxml import html
import sys
import json
import requests
import re

OUT_HTML = 'data/likes.html'
OUT_JSON = 'data/likes.json'
IN_TEMPLATE = 'template.html'
IN_COOKIES = 'cookies.txt'

GET_ROOT = 'http://www.pandora.com'
GET_LIKES = 'http://www.pandora.com/content/tracklikes?webname={username}&thumbStartIndex={index}'
GET_LIKES_CNT = 5   # number of likes returned per request


def scrape_user(username, max_recent=sys.maxint, save_html=True, save_json=True):
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
    likes = remove_duplicates(likes)
    print("Got {} song likes".format(len(likes)))

    if save_json:
        save_json_file(username, likes)
    if save_html:
        save_html_file(username, likes)

    return likes


def remove_duplicates(likes):
    def same(a, b, name):
        return a[name] != u'?' and a[name] == b[name]

    filtered = list()
    for like in likes:
        seen = False
        for f in filtered:
            if same(like, f, 'song') and same(like, f, 'album') and same(like, f, 'artist'):
                seen = True
                break
        if not seen:
            filtered.append(like)

    print("Removed {} duplicates".format(len(likes) - len(filtered)))
    return filtered


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

        if like['audioFile'] == u'$track.getSampleUrl(true)':
            like['audioFile'] = '#'

        if like['album'] == '?':
            like['album'] = clean(song_root.xpath("//span[contains(@class, 'album_link')]/text()"))

        likes.append(like)

    return likes


def save_json_file(username, likes):
    data = dict()
    data['likes'] = likes
    data['username'] = username

    fo = open(OUT_JSON, 'w')
    fo.write(json.dumps(data, indent=4))
    fo.close()


def save_html_file(username, likes):
    # Load template
    template = open(IN_TEMPLATE, 'r')
    in_html = u''.join(template.readlines())
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
    fo.write(in_html.encode("UTF-8"))
    fo.close()


def html_from_json(file_name):
    global OUT_HTML
    OUT_HTML = str(file_name).replace('.json', '') + '.html'

    fi = open(file_name)
    j = json.loads(''.join(fi.readlines()))
    fi.close()

    save_html_file(j['username'], remove_duplicates(j['likes']))


if __name__ == '__main__':
    argc = len(sys.argv)

    if argc <= 1:
        scrape_user(str(input('Enter the pandora user to scrape likes from: ')))
    else:
        scrape_user(
            sys.argv[1],
            int(sys.argv[2]) if argc >= 3 and str(sys.argv[2]).isdigit() else sys.maxint,
            (str(sys.argv[3]).lower() == 'true') if argc >= 4 else True,
            (str(sys.argv[4]).lower() == 'true') if argc >= 5 else True,
        )


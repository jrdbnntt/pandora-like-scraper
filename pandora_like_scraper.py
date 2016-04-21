#!/usr/bin/python

from __future__ import print_function
import sys
import json

OUT_HTML = 'likes.html'
OUT_JSON = 'likes.json'
IN_TEMPLATE = 'template.html'

GET_LIKES = 'www.pandora.com/content/tracklikes?webname={}&thumbStartIndex={}'
LIKES_PER_INDEX = 5     # number of likes pandora gives you each get


def scrape_user(username, save_html=True, save_json=True, max_recent=sys.maxint):
    """ Scrapes pandora likes from user """
    print('Scraping pandora likes from {}...'.format(username))

    likes = list()

    # Get all likes
    i = 0
    while i < max_recent:
        new = get_like_index(username, i)

        if len(new) == 0:
            break

        likes.extend(new)
        i += 1

    # Remove excess
    while len(likes) > max_recent:
        likes.pop(len(likes)-1)

    # Remove duplicates
    for i in range(0, len(likes)):
        if i != len(likes)-2:
            for j in range(i+1, len(likes)):
                if likes[i].song == likes[j].song:
                    likes.pop(j)

    if save_html:
        save_json_file(likes)
    if save_json:
        save_html_file(username, likes)

    return likes


def get_like_index(username, index):
    """ Pulls info from each in the index """
    return []


def scrape_like(html):
    pass


def save_json_file(likes):
    data = dict()
    data['likes'] = likes

    fo = open(OUT_JSON, 'w')
    fo.write(json.dumps(data, indent=4))
    fo.close()


def save_html_file(username, likes):
    # Load template
    template = open(IN_TEMPLATE, 'r')
    html = '\n'.join(template.readlines())
    template.close()

    # Create rows
    rows = list()
    for like in likes:
        row = '<tr>'
        row += '<td>' + like['artist'] + '</td>'
        row += '<td>' + like['album'] + '</td>'
        row += '<td>' + like['albumArt'] + '</td>'
        row += '<td>' + like['song'] + '</td>'
        row += '</tr>'
        rows.append(row)

    # Save as html
    fo = open(OUT_HTML, 'w')
    fo.write(html.format(username=username, rows=' '.join(rows)))
    fo.close()


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 1:
        scrape_user(str(input('Enter the pandora user to scrape likes from: ')))
    else:
        count = l
        scrape_user(
            sys.argv[0],
            (sys.argv[1] == 'True') if argc >= 2 else True,
            (sys.argv[2] == 'True') if argc >= 3 else True,
            int(sys.argv[3]) if argc >= 4 and str(sys.argv[3]).isdigit() else sys.maxint
        )




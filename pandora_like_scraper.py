#!/usr/bin/python

from __future__ import print_function
import sys


GET_LIKES = 'www.pandora.com/content/tracklikes?webname={}&thumbStartIndex={}'
OUT_HTML = 'likes.html'
LIKES_PER_INDEX = 5     # number of likes pandora gives you each get


def scrape_user(username, html=True, json=True, max_recent=sys.maxint):
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

    if html:
        save_json(likes)
    if json:
        save_html(likes)

    return likes


def get_like_index(username, index):
    """ Pulls info from each in the index """
    return []


def scrape_like(html):
    pass


def save_json(likes):
    pass


def save_html(likes):
    pass

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




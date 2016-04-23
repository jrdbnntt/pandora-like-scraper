"""
    Tool for managing a populated likes.json
"""

from __future__ import print_function
import sys
import pandora_like_scraper as ps
import json

BK_JSON = ps.OUT_JSON.replace('likes.', 'bk.likes.')
BK_HTML = ps.OUT_HTML.replace('likes.', 'bk.likes.')


def manage(function, *args):
    def default(*args):
        print("Invalid command", function, *args)

    {
        'backup': backup,
        'remove': remove,
        'restore': restore,
    }.get(function, default)(*args)


def load_json():
    fi = open(ps.OUT_JSON, 'r')
    data = json.loads(''.join(fi.readlines()))
    fi.close()
    return data


def save(data):
    ps.save_json_file(ps.OUT_JSON, data['username'], data['likes'])
    ps.save_html_file(ps.OUT_HTML, data['username'], data['likes'])


def backup():
    data = load_json()
    ps.save_json_file(BK_JSON, data['username'], data['likes'])
    ps.save_html_file(BK_HTML, data['username'], data['likes'])


def restore():
    fi = open(BK_JSON, 'r')
    data = json.loads(''.join(fi.readlines()))
    fi.close()
    save(data)


def remove(order):
    data = load_json()
    order = int(order)
    for like in data['likes']:
        if like['order'] == order:
            data['likes'].remove(like)
            save(data)
            print("Removed '{}' by '{}' on '{}'".format(like['song'], like['artist'], like['album']))
            return
    print("Song with order {} not found".format(order))


if __name__ == '__main__':
    manage(*sys.argv[1:])


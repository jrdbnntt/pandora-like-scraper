Pandora Like Scraper
====================

Scrapes all info about a pandora user's likes and exports them into a nice web page format. Due to the way pandora
provides the likes, the order returned will be from most to least recently liked songs. Since it uses your existing
pandora cookies, it is safe to say using this method to copy a ton of music files is probably a bad idea. I've included
the links just as a way to test the track.

Requires two files:
* `template.html` - in repo, html template
* `cookies.txt` - copy your cookies from a xhr request pandora does to itself while you are logged in into this file in standard header format (`name=val; name=val;`...)

Creates two files:
* A `likes.html` web page that has all the likes in a nice display format
* A `likes.json` file that has the likes in the format below

JSON format
```json
{
  "likes": [
    {
      "artist": "Artist name 1",
      "album": "Album name 1",
      "albumArt": "http://pandora.com/path/to/static/image.jpg",
      "song": "Song name 1"
    }
  ]
}
```

Can be used via command line, where the command line args are passed into the following function, in order:
```python
def scrape_user(username, save_html=True, save_json=True, max_recent=sys.maxint)
```

When saving the html file and calling the function where `template.html` is not in the working directory, set the module
constant `IN_TEMPLATE` to it's relative path, or to your own template page.

I made this for myself because I use my likes from pandora to choose what albums to get later. Feel free to use it for
whatever.
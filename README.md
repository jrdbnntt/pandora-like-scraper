Pandora Like Scraper
====================

Scrapes all info about a pandora user's likes and exports them into a nice web page format. Due to the way pandora
provides the likes, the order returned will be from most to least recently liked songs.

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
def scrape_user(username, html=True, json=True, max_recent=sys.maxint)
```
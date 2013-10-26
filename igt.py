import urllib, re, sys, os
from BeautifulSoup import BeautifulSoup, Tag

# UTILITIES:

def soup_scoup(url):
    raw = urllib.urlopen(url).read()
    return BeautifulSoup(raw)
def mkdir(dir):
    try:
        os.mkdir(dir)
        return True
    except OSError:
        return False
def string_to_file(file, string):
    print "Writing out %s" % file
    with open(file, "w") as f:
        f.write(string)
    
# EXTERNAL URLS:

def ext_artist_cloud_url():
    return "http://www.indieguitartabs.com/artist-cloud.html"
def ext_artist_url(artist):
    return "http://www.indieguitartabs.com/bands/%s/" % artist
def ext_song_url(artist, song):
    return "http://www.indieguitartabs.com/bands/%s/%s.html" % (artist, song)

# GLOBALS:

outdir = "igt"

# GRABBIN'-CODE

def grab_artist(artist):
    def grab_song(song):
        soup = soup_scoup(ext_song_url(artist, song))
        string_to_file("%s/%s/tabs/%s.html" % (outdir, artist, song),
                       soup.findAll("pre")[0].prettify())
    
    if not mkdir("%s/%s" % (outdir, artist)):
        return
    mkdir("%s/%s/tabs" % (outdir, artist))
    soup = soup_scoup(ext_artist_url(artist))
    
    albumList = soup.find(id="albumList")
    for link in albumList.findAll("a"):
        song_res = re.findall("/bands/%s/(.*).html" % artist, link['href'])
        if len(song_res) > 0:
            song = song_res[0]
            link['href'] = "tabs/%s.html" % (song)
            grab_song(song)
    for image in albumList.findAll("img"):
        image.extract()
    string_to_file("%s/%s/index.html" % (outdir, artist),
                   albumList.prettify())

def grab_all():
    soup = soup_scoup(ext_artist_cloud_url())
    links = soup.findAll(attrs="tag")
    out = "<ul>"
    for link in links:
        artist = link["href"].replace("/bands/","").replace("/","")
        label = link.text
        out += '<li><a href="%s/index.html">%s</a></li>' % (artist, label)
        grab_artist(artist)
    out += "</ul>"

    mkdir(outdir)
    string_to_file("%s/index.html" % outdir, out)

grab_all()

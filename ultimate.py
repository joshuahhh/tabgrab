import urllib, re, sys, os, glob
from BeautifulSoup import BeautifulSoup, Tag
from collections import defaultdict

rewrite_all = False

in_dir = "ultimate-in"
out_dir = "ultimate-out"

in_files = glob.glob("%s/*.htm" % in_dir)

index = defaultdict(list)

for f in in_files:
    soup = BeautifulSoup(open(f).read())
    updmsg = soup.find('div', {'class':'updmsg'})
    name = updmsg.find('strong').text
    artist = updmsg.find('b').text

    artist_dir = "%s/%s" % (out_dir, artist)
    if not os.path.exists(artist_dir):
        os.makedirs(artist_dir)

    song_file = "%s/%s.html" % (artist_dir, name)
    if not os.path.exists(song_file) or rewrite_all:
        with open(song_file, 'w') as f:
            f.write(str(soup.findAll('pre')[-1]))

    index[artist].append((name, song_file))

out = "<ul>"
for artist, songs in sorted(index.items()):
    out += "<li>%s<ul>" % artist
    for song, song_file in sorted(songs):
        out += "<li><a href='../%s'>%s</a></li>" % (song_file, song)
    out += "</ul></li>"
out += "</ul>"

with open("%s/index.html" % out_dir, 'w') as f:
    f.write(out)

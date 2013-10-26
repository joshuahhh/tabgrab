# TODO: make directories!

import urllib, re

def make_url(name):
    return "http://themountaingoats.net/wiki/doku.php?id=tabs:%s&do=export_html" % name

outdir = "mg"

raw = urllib.urlopen(make_url("home")).read()
names = re.findall('/wiki/doku.php\?id=tabs:([^"=]*)"', raw)
with open("%s/index.html" % outdir, 'w') as f:
    f.write(re.sub('/wiki/doku.php\?id=tabs:([^"]*)', 'tabs/\\1.html', raw))
for name in names:
    print "grabbing %s" % name
    urllib.urlretrieve(make_url(name), "%s/tabs/%s.html" % (outdir, name))

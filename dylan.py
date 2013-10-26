import urllib, re, sys, os
from BeautifulSoup import BeautifulSoup, Tag

outdir = "dylan"

indexfile = "%s/index.html" % outdir

if not os.path.exists(indexfile):
    if not os.path.exists(os.path.dirname(indexfile)):
        os.makedirs(os.path.dirname(indexfile))
    print "downloading index"
    urllib.urlretrieve("http://dylanchords.info/alphabetical_list_of_songs.htm",
                       indexfile)
    print "  done"

indexraw = open(indexfile).read()

for filename in re.findall("([a-z_0-9]*/.*\.htm)", indexraw):
    print filename
    local_filename = "%s/%s" % (outdir, filename)
    if not os.path.exists(local_filename):
        if not os.path.exists(os.path.dirname(local_filename)):
            os.makedirs(os.path.dirname(local_filename))
        urllib.urlretrieve("http://dylanchords.info/%s" % filename,
                           local_filename)

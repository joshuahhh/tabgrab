import os

import requests

out_dir = "tmbg"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

def get_pages_in_category(api_url, category_title, cmcontinue=None):
    params = dict(
        action = "query",
        list = "categorymembers",
        cmtitle = category_title,
        cmlimit = "max",
        format = "json",
        )
    if cmcontinue:
        params['cmcontinue'] = cmcontinue

    response = requests.get(api_url, params=params).json()
    categorymembers = response["query"]["categorymembers"]
    results = [member["title"] for member in categorymembers]

    try:
        cmcontinue = response["query-continue"]["categorymembers"]["cmcontinue"]
        results += get_pages_in_category(api_url, category_title, cmcontinue)
    except KeyError:
        pass

    return results

titles = [s[11:].encode("utf8")
          for s in get_pages_in_category("http://tmbw.net/wiki/api.php",
                                         "Category:Guitar_Tabs")
          if s.startswith("Guitar Tab:")]

print "Found %i tabs!" % len(titles)

for title in titles:
    print title

    filename = "%s/%s.html" % (out_dir, title)
    if not os.path.exists(filename):
        params = dict(action = "raw", title = "Guitar Tab:" + title)
        g = requests.get("http://tmbw.net/wiki/index.php", params=params)
        with open(filename, 'w') as f:
            f.write("<meta charset='utf-8'><pre>")
            f.write(g.text.encode('utf8'))
            f.write("</pre>")


out = "<meta charset='utf-8'><ul>"
for title in titles:
    out += "<li><a href='%s.html'>%s</a></li>" % (title, title)
out += "</ul>"
            
with open("%s/index.html" % out_dir, 'w') as f:
    f.write(out)

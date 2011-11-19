#! /usr/bin/env python2.6

import sys, feedparser, urllib2
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from xml.sax.saxutils import escape

if len(sys.argv) > 1:
    gc_rss_url = sys.argv[1]
else:
    sys.exit(1)

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1'
#gc_rss_url = "http://feeds.feedburner.com/uclick/toby"
gc_feed = feedparser.parse(gc_rss_url)

print '<?xml version="1.0" encoding="utf-8"?>'
print '<feed xmlns="http://www.w3.org/2005/Atom">'
print '<title>%s</title>' % escape(gc_feed['feed']['title'])
print '<link href="%s" rel="alternate"/>' % escape(gc_feed['feed']['link'])
print '<id>%s</id>' % escape(gc_feed['feed']['link'])
print '<updated>%s</updated>' % escape(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
 
for i in gc_feed.entries:
    if 'feedburner_origlink' in i.keys():
        link = i.feedburner_origlink
    else:
        link = i.link
    url_req = urllib2.Request(link, headers = {'User-Agent' : user_agent})
    url = urllib2.urlopen(url_req)
    soup = BeautifulSoup(url)
    tag = None
    tag = soup.find('img', {'class' : 'strip'})
    if tag is not None and tag.has_key('src') :
        image = tag['src'] 
    else:
        print >> sys.stderr, 'Image not found in ' + url
        continue

    print '<entry>'
    print '<title>%s</title>' % escape(i.title)
    print '<link href="%s" rel="alternate"/>' % escape(link)
    print '<id>%s</id>' % escape(link)
    print '<summary type="xhtml">'
    print '<div xmlns="http://www.w3.org/1999/xhtml">'
    print '<img src="%s" />' % escape(image) 
    print '</div>'
    print '</summary>'
    print '</entry>'

print '</feed>'

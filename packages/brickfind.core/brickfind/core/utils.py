# vim: set fileencoding=utf8:
"""
short module explanation

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
__VERSION__ = "0.1.0"
from lxml import etree
from brickfind.db import fetch_brick

def update_db(xmlurl):
    """update db via xml file"""
    URL_PATTERN = r"http://partsregistry.org/cgi/xml/part.cgi?part=%s"
    context = etree.iterparse(xmlurl, events=('end',), tag='SEGMENT')

    urls = []
    print "Parsing..."
    for event, elem in context:
        name = elem.text.encode('utf-8')
        url = URL_PATTERN % name
        urls.append(url)
    size = len(urls)
    print "Download %d brick informations..." % size
    for i, url in enumerate(urls[:10]):
        brick = fetch_brick(url).next()
        print "%s information has downloaded (%d/%d)" % (brick, i+1, size)

def main():
    """for speed test
    
    How to visualize stats file::

        >>> import pstats
        >>> p = pstats.Stats('utils.sqlite.stats')
        >>> p.sort_stats('time').print_stats(10)

    """
    
    from brickfind.db.sessions import create_session

    # result = utils.sqlite.stats
    create_session('sqlite:///sample.db')
    # result = utils.mysql.stats
    #create_session('mysql://root@localhost/brickfind_db_dev')
    import os.path
    update_db(os.path.join(os.path.dirname(__file__), 'tests/entry_points.xml'))

if __name__ == '__main__':
    main()



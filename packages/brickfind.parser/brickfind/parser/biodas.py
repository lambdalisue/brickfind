# vim: set fileencoding=utf8:
"""
parser module of biodas format entry points

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
from lxml import etree      # Use lxml for highspeed analysis
from itertools import islice

def fastiter(context, fn):
    """fast iteration for lxml iterparse"""
    for event, element in context:
        fn(element)
        element.clear()
        while element.getprevious() is not None:
            del element.getparent()[0]
    del context

PARTSREGISTRY_URL_PATTERN = r"http://partsregistry.org/cgi/xml/part.cgi?part=%s"
def create_entry_point(name):
    url = PARTSREGISTRY_URL_PATTERN%name
    return (name, url)

def parse(uri, size=None):
    """parse biodas entry points xml"""
    context = etree.iterparse(uri, events=('end',), tag='SEGMENT')
    if size:
        context = islice(context, size)

    entry_points = []
    def fn(e):
        name = e.text.encode('utf-8')
        entry_points.append(create_entry_point(name))

    # execute
    fastiter(context, fn)

    return entry_points

# vim: set fileencoding=utf8:
"""
brickfind.parser module

This module is used to parse xml of `MIT registry of standard 
biological parts <http://partsregistry.org/Main_Page>`_

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

from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from datetime import datetime
from itertools import islice

def _get_string(x):
    return x.string.strip() if x.string else ""
def _get_int(x):
    return int(x.string) if x.string else None
def _get_date(x):
    return datetime.strptime(x.string, "%Y-%m-%d") if x.string else None

def _build_feature(soup):
    feature = {}
    feature['title'] = _get_string(soup.title)
    feature['type'] = _get_string(soup.type)
    feature['direction'] = _get_string(soup.direction).lower()
    feature['startpos'] = _get_int(soup.startpos)
    feature['endpos'] = _get_int(soup.endpos)
    return feature
def _build_brick(soup):
    brick = {}
    brick['name'] = _get_string(soup.part_name)
    brick['nickname'] = _get_string(soup.part_nickname)
    brick['description'] = _get_string(soup.part_short_desc)
    brick['type'] = _get_string(soup.part_type)
    brick['status'] = _get_string(soup.part_status).lower()
    brick['results'] = _get_string(soup.part_results).lower()
    brick['rating'] = _get_int(soup.part_rating)
    brick['url'] = _get_string(soup.part_url)
    brick['publish_at'] = _get_date(soup.part_entered)
    brick['author'] = _get_string(soup.part_author)
    brick['quality'] = _get_string(soup.best_quality).lower()
    lst = []
    for sequence in soup.sequences('seq_data'):
        lst.append(_get_string(sequence))
    brick['sequences'] = tuple(lst)
    lst = []
    for feature in soup.features('feature'):
        lst.append(_build_feature(feature))
    brick['features'] = tuple(lst)
    return brick

def parse(url, size=10):
    """parse xml of the MIT Registry of Standard Biological Parts to python
    dictionary instance
    
    You can get dictionary based brick information via 'parse' function

        >>> from brickfind.parser import parse

    This function get url and return iterator of bricks

        >>> import os.path
        >>> ibricks = parse(os.path.join(os.path.dirname(__file__),
        ...     'tests/BBa_B0034.xml'))
        >>> for brick in ibricks:
        ...     brick['name']
        u'BBa_B0034'

    A structure of each bricks returned is shown below:

        - name
        - nickname
        - description
        - type
        - status
        - results
        - rating [int]
        - url
        - publish_at [datetime]
        - author
        - quality
        - sequences [list]
        - features [list]
          - title
          - type
          - direction
          - startpos [int]
          - endpos [int]

    """
    if url.startswith('http'):
        xml = urlopen(url)
    else:
        xml = open(url)
    soup = BeautifulSoup(xml)
    soup = soup.rsbpml.part_list
    for brick in islice(soup('part'), size):
        yield _build_brick(brick)

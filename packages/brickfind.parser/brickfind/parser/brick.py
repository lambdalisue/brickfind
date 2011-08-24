# vim: set fileencoding=utf8:
"""
parser module of the MIT Standard Biological Parts Registry xml

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
import re
from urllib2 import urlopen
from itertools import islice
from datetime import datetime
from .utils import Attrdict
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

_PROTOCOL_PATTERNS = re.compile(r"(?:http[s]|ftp)://.*")
def uriopen(uri):
    """open file or url and return stream object"""
    if _PROTOCOL_PATTERNS.match(uri):
        method = urlopen
    else:
        method = open
    return method(uri)

def lazystr(x):
    """call strip() function of instance if x is string"""
    x = x.string if hasattr(x, 'string') else x
    if isinstance(x, basestring):
        return x.strip()
    # Do nothing if x is not string
    return x
def lazyint(x):
    """try to convert x to int"""
    x = lazystr(x)
    try:
        return int(x)
    except:
        # TODO: filter with proper Error
        # Fail silently
        return x
DATE_FORMAT="%Y-%m-%d"
def lazydate(x):
    """try to convert x to date"""
    x = lazystr(x)
    if isinstance(x, basestring):
        return datetime.strptime(x, DATE_FORMAT)
    return x

def parse(uri, size=None):
    """parse xml of the MIT Registry of Standard Biological Parts
    
    How to use::

        >>> from brickfind.parser.brick import parse
        >>> # Load xml from filesystem
        >>> import os.path
        >>> uri = os.path.join(
        ...     os.path.dirname(__file__),
        ...     'tests/BBa_B0034.xml')
        >>> brick_infos = parse(uri, 10)
        >>> len(brick_infos)
        1
        >>> brick_info = brick_infos[0]
        >>> brick_info.name
        u'BBa_B0034'
        >>> brick_info.type
        u'RBS'

    Return:

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
        - categories [list]
              
    """
    response = uriopen(uri)
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response)
    bricks = soup.rsbpml.part_list('part')
    if size:
        bricks = islice(bricks, size)
    brick_infos = []
    for brick in bricks:
        # Create sequence list
        sequence_list = []
        for sequence in brick.sequences('seq_data'):
            sequence_list.append(lazystr(sequence))
        # Create feature list
        feature_list = []
        for feature in brick.features('feature'):
            feature_list.append({
                'title': lazystr(feature.title),
                'type': lazystr(feature.type),
                'direction': lazystr(feature.direction),
                'startpos': lazyint(feature.startpos),
                'endpos': lazyint(feature.endpos),
            })
        # Create category list
        category_list = []
        for category in brick.categories('category'):
            category_list.append(lazystr(category))
        # Create brick
        brick_info = Attrdict({
            'name': lazystr(brick.part_name),
            'nickname': lazystr(brick.part_nickname),
            'description': lazystr(brick.part_short_desc),
            'type': lazystr(brick.part_type),
            'status': lazystr(brick.part_status),
            'results': lazystr(brick.part_results),
            'rating': lazyint(brick.part_rating),
            'url': lazystr(brick.part_url),
            'publish_at': lazydate(brick.part_entered),
            'author': lazystr(brick.part_author),
            'quality': lazystr(brick.best_quality),
            'sequences': tuple(sequence_list),
            'features': tuple(feature_list),
            'categories': tuple(category_list),
        })
        brick_info._mutable = False
        brick_infos.append(brick_info)
    return brick_infos

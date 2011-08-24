# vim: set fileencoding=utf8:
"""
Unittest module of ...

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
from datetime import datetime
from nose.tools import eq_, ok_
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from ..models import Brick, Sequence, Feature, Category

session = None
def setup():
    global session
    session = scoped_session(sessionmaker())

def teardown():
    session.remove()

def test_category():
    dict_info = {
        'label': 'foobar',
        'parent_id': None,
    }
    new = Category(**dict_info)
    eq_(new.label, dict_info['label'])
    eq_(new.parent_id, dict_info['parent_id'])

    dict_info2 = {
        'label': 'hogehoge',
        'parent_id': new.id
    }
    new2 = Category(**dict_info2)
    eq_(new2.label, dict_info2['label'])
    eq_(new2.parent_id, dict_info2['parent_id'])

def test_category_cpath_find():
    # CPath Creation
    dict_info = {
        'cpath': '//chassis/prokaryote/ecoli',
    }
    new = Category.find(**dict_info)
    eq_(new.label, 'ecoli')
    eq_(new.parent.label, 'prokaryote')
    eq_(new.parent.parent.label, 'chassis')
    eq_(new.parent.parent.parent, None)

def test_category_cpath_get():
    dict_info = {
        'cpath': '//chassis/prokaryote/ecoli',
    }
    new = Category.find(**dict_info)
    eq_(new.cpath, '//chassis/prokaryote/ecoli')

def test_category_cpath_set():
    dict_info = {
        'cpath': '//chassis/prokaryote/ecoli',
    }
    new = Category.find(**dict_info)
    new.cpath = '//chassis/prokaryote2/ecoli2'
    eq_(new.label, 'ecoli2')
    eq_(new.parent.label, 'prokaryote2')
    eq_(new.parent.parent.label, 'chassis')
    eq_(new.parent.parent.parent, None)


def test_feature():
    dict_info = {
        'title': None,
        'type': 'conserved',
        'direction': 'forward',
        'startpos': 5,
        'endpos': 8
    }
    new = Feature(**dict_info)
    eq_(new.title, dict_info['title'])
    eq_(new.type, dict_info['type'])
    eq_(new.direction, dict_info['direction'])
    eq_(new.startpos, dict_info['startpos'])
    eq_(new.endpos, dict_info['endpos'])

def test_sequence():
    dict_info = {
        'sequence': 'aaagaggagaaa',
    }
    new = Sequence(**dict_info)
    eq_(new.sequence, dict_info['sequence'])
def test_sequence_complement_get():
    dict_info = {
        'sequence': 'aaagaggagaaa',
    }
    new = Sequence(**dict_info)
    eq_(new.complement, 'tttctcctcttt')
def test_sequence_complement_set():
    dict_info = {
        'sequence': 'aaagaggagaaa',
    }
    new = Sequence(**dict_info)
    new.complement = 'aaagaggagaaa'
    eq_(new.sequence, 'tttctcctcttt')


def test_brick():
    dict_info = {
        'name': 'BBa_B0034',
        'nickname': None,
        'description': 'RBS (Elowitz 1999) -- defines RBS efficiency',
        'type': 'RBS',
        'status': 'Available',
        'results': 'Works',
        'rating': 1,
        'url': 'http://partsregistry.org/Part:BBa_B0034',
        'publish_at': datetime.strptime('2003-01-31', '%Y-%m-%d'),
        'author': 'Vinay S Mahajan, Voichita D. Marinescu, Brian Chow,' 
            ' Alexander D Wissner-Gross and Peter Carr IAP, 2003.',
        'quality': 'Confirmed',
    }
    new = Brick(**dict_info)
    eq_(new.name, dict_info['name'])
    eq_(new.nickname, dict_info['nickname'])
    eq_(new.description, dict_info['description'])
    eq_(new.status, dict_info['status'])
    eq_(new.results, dict_info['results'])
    eq_(new.rating, dict_info['rating'])
    eq_(new.url, dict_info['url'])
    eq_(new.publish_at, dict_info['publish_at'])
    eq_(new.author, dict_info['author'])
    eq_(new.quality, dict_info['quality'])

def test_brick_factory():
    dict_info = {
        'name': 'BBa_B0034',
        'nickname': None,
        'description': 'RBS (Elowitz 1999) -- defines RBS efficiency',
        'type': 'RBS',
        'status': 'Available',
        'results': 'Works',
        'rating': 1,
        'url': 'http://partsregistry.org/Part:BBa_B0034',
        'publish_at': datetime.strptime('2003-01-31', '%Y-%m-%d'),
        'author': 'Vinay S Mahajan, Voichita D. Marinescu, Brian Chow,' 
            ' Alexander D Wissner-Gross and Peter Carr IAP, 2003.',
        'quality': 'Confirmed',
        'sequences': [
            'aaagaggagaaa',
        ],
        'features': [{
            'title': None,
            'type': 'conserved',
            'direction': 'forward',
            'startpos': 5,
            'endpos': 8
        }],
        'categories': [
            '//chassis/prokaryote/ecoli',
            '//direction/forward',
            '//function/coliroid',
            '//rbs/prokaryote/constitutive/community',
            '//regulation/constitutive',
            '//ribosome/prokaryote/ecoli',
        ],
    }
    new, created = Brick.factory(dict_info)
    eq_(created, True)
    ok_(isinstance(new, Brick))

if __name__ == '__main__':
    import nose
    nose.main()

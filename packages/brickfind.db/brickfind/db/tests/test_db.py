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
import yaml
import os.path
from nose.tools import ok_, eq_, nottest
from ..sessions import create_session
from ..models import Brick
from .. import update_brick, fetch_brick

default_sequence_datas = None
default_feature_datas = None
default_brick_data = None

def setup():
    create_session('sqlite://')

    # Load default each datas from fixture
    path = os.path.join(
            os.path.dirname(__file__),
            'fixtures/test_%s.yaml')
    global default_sequence_datas
    default_sequence_datas = [yaml.load(open(path%"sequence"))]
    global default_feature_datas
    default_feature_datas = [yaml.load(open(path%"feature"))]
    global default_brick_data
    default_brick_data = yaml.load(open(path%"brick"))

def combine_datas(brick_data=None, sequence_datas=None, 
        feature_datas=None):
    brick_data = brick_data or default_brick_data
    sequence_datas = sequence_datas or default_sequence_datas
    feature_datas = feature_datas or default_feature_datas
    brick_data = dict(brick_data)
    brick_data['sequences'] = list(sequence_datas)
    brick_data['features'] = list(feature_datas)
    return brick_data

@nottest
def test_brick_attributes(instance, brick_data=None, sequence_datas=None,
        feature_datas=None):
    brick_data = brick_data or default_brick_data
    sequence_datas = sequence_datas or default_sequence_datas
    feature_datas = feature_datas or default_feature_datas

    for key, value in brick_data.iteritems():
        if key == 'categories':
            lhs = [category.get_full_label() for category in instance.categories]
            eq_(lhs, value)
        else:
            eq_(getattr(instance, key), value)
    for i,sequence in enumerate(sequence_datas):
        for key, value in sequence.iteritems():
            eq_(getattr(instance.sequences[i], key), value)
    for i,feature in enumerate(feature_datas):
        for key, value in feature.iteritems():
            eq_(getattr(instance.features[i], key), value)
    
def test_update_brick_create():
    """make sure the update_brick create new brick"""
    data = combine_datas()
    new = update_brick(data)

    # Instance check
    ok_(isinstance(new, Brick))
    # Attribute check
    test_brick_attributes(new)

def test_update_brick_difference():
    """make sure the update_brick create different brick"""
    from datetime import date
    data = combine_datas()
    new = update_brick(data)

    brick_data = {
            'name': 'BBa_FOOBAR',
            'description': 'Test additional parts',
            'type': 'TEST',
            'status': 'Notavariable',
            'results': 'Hopefully work',
            'nickname': 'Hello world',
            'rating': 1,
            'url': 'http://www.google.com/',
            'publish_at': date(2000, 01, 01),
            'author': 'lambdalisue',
            'quality': 'confirmed',
        }
    sequence_datas = [
            {'sequence': """aaaaaaaaaaaaaaaaaaaaa"""},
            {'sequence': """ttttttttttttttttttttt"""},
        ]
    feature_datas = [
            {'title': 'foobar', 'type': 'conserved', 'direction': 'forward',
                'startpos': 10, 'endpos': 20},
            {'title': 'hogehoge', 'type': 'pyapya', 'direction': 'reverse',
                'startpos': 2, 'endpos': 5},
        ]
    data2 = combine_datas(brick_data, sequence_datas, feature_datas)
    new2 = update_brick(data2)

    test_brick_attributes(new2, brick_data, sequence_datas, feature_datas)

    assert new != new2, "%r == %r" % (new, new2)

def test_update_brick_update():
    """make sure update_brick update featrue work"""
    from datetime import date
    data = combine_datas()
    new = update_brick(data)

    brick_data = {
            'name': new.name,
            'description': 'Test additional parts',
            'type': 'TEST',
            'status': 'Notavariable',
            'results': 'Hopefully work',
            'nickname': 'Hello world',
            'rating': 1,
            'url': 'http://www.google.com/',
            'publish_at': date(2000, 01, 01),
            'author': 'lambdalisue',
            'quality': 'confirmed',
        }
    sequence_datas = [
            {'sequence': """aaaaaaaaaaaaaaaaaaaaa"""},
            {'sequence': """ttttttttttttttttttttt"""},
        ]
    feature_datas = [
            {'title': 'foobar', 'type': 'conserved', 'direction': 'forward',
                'startpos': 10, 'endpos': 20},
            {'title': 'hogehoge', 'type': 'pyapya', 'direction': 'reverse',
                'startpos': 2, 'endpos': 5},
        ]
    data2 = combine_datas(brick_data, sequence_datas, feature_datas)
    new2 = update_brick(data2)

    test_brick_attributes(new2, brick_data, sequence_datas, feature_datas)

    eq_(new, new2)

def test_fetch_brick_create():
    """make sure fetch brick feature work"""
    url = r"http://partsregistry.org/xml/part.BBa_B0034"
    new = fetch_brick(url).next()

    test_brick_attributes(new)

if __name__ == '__main__':
    import nose
    nose.main()

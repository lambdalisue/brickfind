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
import os.path
from nose.tools import eq_, raises
from ..brick import parse, lazydate

def test_parse():
    uri = os.path.join(
            os.path.dirname(__file__),
            'BBa_B0034.xml')
    brick_infos = parse(uri)
    eq_(len(brick_infos), 1)

    bi = brick_infos[0]
    eq_(bi.name, 'BBa_B0034')
    eq_(bi.nickname, None)
    eq_(bi.description, 'RBS (Elowitz 1999) -- defines RBS efficiency')
    eq_(bi.type, 'RBS')
    eq_(bi.status, 'Available')
    eq_(bi.results, 'Works')
    eq_(bi.rating, 1)
    eq_(bi.url, 'http://partsregistry.org/Part:BBa_B0034')
    eq_(bi.publish_at, lazydate('2003-01-31'))
    eq_(bi.author, 'Vinay S Mahajan, Voichita D. Marinescu, Brian Chow, Alexander      D Wissner-Gross and Peter Carr IAP, 2003.')
    eq_(bi.quality, 'Confirmed')
    eq_(bi.sequences, (
            'aaagaggagaaa',
        ))
    eq_(bi.features, ({
            'title': None,
            'type': 'conserved',
            'direction': 'forward',
            'startpos': 5,
            'endpos': 8,
        },))
    eq_(bi.categories, (
            '//chassis/prokaryote/ecoli',
            '//direction/forward',
            '//function/coliroid',
            '//rbs/prokaryote/constitutive/community',
            '//regulation/constitutive',
            '//ribosome/prokaryote/ecoli',
        ))

@raises(AttributeError)
def test_parse_immutable():
    uri = os.path.join(
            os.path.dirname(__file__),
            'BBa_B0034.xml')
    brick_infos = parse(uri)
    eq_(len(brick_infos), 1)

    bi = brick_infos[0]
    bi.name = "this action call AttributeError"

if __name__ == '__main__':
    import nose
    nose.main()

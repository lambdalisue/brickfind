# vim: set fileencoding=utf8:
"""
Unittest module of brickfind.parser

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
from nose.tools import eq_
import os.path
from datetime import datetime
from .. import parse

def test_parse():
    EXPECTED = dict(
        name="BBa_B0034",
        description="RBS (Elowitz 1999) -- defines RBS efficiency",
        type="RBS",
        status="Available",
        results="Works",
        nickname=None,
        rating=1,
        url="http://partsregistry.org/Part:BBa_B0034",
        publish_at=datetime.strptime("2003-01-31", "%Y-%m-%d"),
        author="Vinay S Mahajan, Voichita D. Marinescu, Brian Chow, " + \
            "Alexander      D Wissner-Gross and Peter Carr IAP, 2003.",
        quality="Confirmed",
        sequences=(
            dict(
                sequence="aaagaggagaaa",
            ),),
        features=(
            dict(
                title=None,
                type="conserved",
                direction="forward",
                startpos=5,
                endpos=8,
            ),),
        categories=(
                'chassis/prokaryote/ecoli',
                'direction/forward',
                'function/coliroid',
                'rbs/prokaryote/constitutive/community',
                'regulation/constitutive',
                'ribosome/prokaryote/ecoli',
            )
        )
    def _check(entry, key, value):
        if isinstance(value, dict):
            for subkey, subvalue in value.iteritems():
                _check(entry[key], subkey, subvalue)
        else:
            eq_(entry[key], value)
    url = os.path.join(os.path.dirname(__file__), r"BBa_B0034.xml")
    res = parse(url)
    entry = res.next()
    for key, value in EXPECTED.iteritems():
        _check(entry, key, value)

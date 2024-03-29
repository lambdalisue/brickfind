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
from nose.tools import eq_
from ..biodas import parse, create_entry_point

def test_parse():
    uri = os.path.join(
            os.path.dirname(__file__),
            'biodas_entry_points.xml')
    entry_points = parse(uri, size=3)
    eq_(len(entry_points), 3)

    eq_(entry_points[0], create_entry_point('BBa_R0050'))
    eq_(entry_points[1], create_entry_point('BBa_R0011'))
    eq_(entry_points[2], create_entry_point('BBa_R0040'))

if __name__ == '__main__':
    import nose
    nose.main()

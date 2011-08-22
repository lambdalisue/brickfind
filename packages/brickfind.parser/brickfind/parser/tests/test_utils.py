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
from nose.tools import eq_, raises
from ..utils import Attrdict

def test_attrdict():
    ad = Attrdict({'foobar': 'hogehoge'})
    eq_(ad['foobar'], ad.foobar)

def test_attrdict_overwrite():
    ad = Attrdict({'foobar': 'hogehoge'})
    ad.foobar = 'piyopiyo'
    eq_(ad['foobar'], 'piyopiyo')
    eq_(ad.foobar, 'piyopiyo')

@raises(AttributeError)
def test_attrdict_immutable():
    ad = Attrdict({'foobar': 'hogehoge'})
    ad._mutable = False
    ad.foobar = 'piyopiyo'

if __name__ == '__main__':
    import nose
    nose.main()

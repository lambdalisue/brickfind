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
from nose.tools import eq_
from ..sessions import create_session
from ..models import Feature
from ..models import Sequence
from ..models import Brick

def setup():
    create_session('sqlite://')

def _test_model(model_class):
    filename = os.path.join(os.path.dirname(__file__),
        'fixtures/test_%s.yaml' % model_class.__name__.lower())
    dict_info = yaml.load(open(filename))
    if 'categories' in dict_info:
        del dict_info['categories']
    result = model_class(**dict_info)
    for key, value in dict_info.iteritems():
        eq_(getattr(result, key), value)

def test_Feature():
    _test_model(Feature)
def test_Sequence():
    _test_model(Sequence)
def test_Brick():
    _test_model(Brick)


if __name__ == '__main__':
    import nose
    nose.main()

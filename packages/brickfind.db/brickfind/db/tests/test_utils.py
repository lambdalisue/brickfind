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
from nose.tools import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..utils import get_or_create_model

Base = declarative_base()
engine = create_engine('sqlite://')

class Hoge(Base):
    __tablename__ = 'hoges'
    id = Column(Integer, primary_key=True)
    foobar = Column(String(20))

metadata = None
session = None
def setup():
    global metadata
    metadata = Base.metadata
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
    global session
    session = Session()

def teardown():
    metadata.drop_all(engine)

def test_get_or_create_model():
    new, created = get_or_create_model(Hoge, {'foobar': 'hogehoge'}, session)
    eq_(created, True)
    
    session.add(new)
    session.flush()

    mod, created = get_or_create_model(Hoge, {'foobar': 'hogehoge'}, session)
    eq_(created, False)


if __name__ == '__main__':
    import nose
    nose.main()

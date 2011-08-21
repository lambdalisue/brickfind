# vim: set fileencoding=utf8:
"""
brickfind.db session module

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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

metadata = Base.metadata
session = None

def create_session(sqluri, global_=True):
    """Creates a session.

    If `global` is True creates a global session variable."""

    engine = create_engine(sqluri)
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
    if global_:
        global session
        session = Session()
        return session
    else:
        return Session()

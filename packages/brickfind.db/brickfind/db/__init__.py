# vim: set fileencoding=utf8:
"""
short module explanation

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
from datetime import datetime
from models import Brick, Sequence, Feature, Category
from models import association_brick_category_table as abc_table
from brickfind.parser import parse

def get_lowest_category(category, session, parent_id=None):
    def _get_or_create_category(label):
        category_query = session.query(Category).filter_by(label=label,
                parent_id=parent_id)
        category_instance = category_query.first()

        if not category_instance:
            category_instance = Category(label=label, parent_id=parent_id)
            session.add(category_instance)
            session.flush()

        return category_instance

    DELIMITER = '/'
    if DELIMITER in category:
        lhs, rhs = category.split(DELIMITER, 1)
        category_instance = _get_or_create_category(lhs)
        return get_lowest_category(rhs, session, category_instance.id)
    else:
        return _get_or_create_category(category)

def update_brick(data, commit=True, session=None):
    """create or update brick via data on to db"""
    from sessions import session as default_session
    if session is None:
        session = default_session

    # backup data because this function will modify data
    _data = dict(data)

    # name column is unique
    brick_query = session.query(Brick).filter_by(name=data['name'])

    if 'sequences' in _data:
        sequences = _data.pop('sequences')
    else:
        sequences = None
    if 'features' in _data:
        features = _data.pop('features')
    else:
        features = None
    if 'categories' in _data:
        categories = _data.pop('categories')
    else:
        categories = None


    brick_instance = brick_query.first()

    if not brick_instance:
        # Create new instance
        brick_instance = Brick(**_data)
    else:
        # Update the instance
        brick_query.update(_data)
        # Remove all sequences and features
        if sequences: session.query(Sequence).filter_by(brick_id=brick_instance.id).delete()
        if features: session.query(Feature).filter_by(brick_id=brick_instance.id).delete()
        # Remove all brick_category associations
        if categories: 
            c = session.connection()
            c.execute(abc_table.delete().where(abc_table.c.brick_id==brick_instance.id))

    # Add sequences and features
    if sequences:
        for seq in sequences:
            sequence = Sequence(**seq)
            brick_instance.sequences.append(sequence)
    if features:
        for fea in features:
            feature = Feature(**fea)
            brick_instance.features.append(feature)
    if categories:
        for category in categories:
            lowest_category = get_lowest_category(category, session)
            brick_instance.categories.append(lowest_category)

    # Add and commit
    if brick_instance.id is None:
        session.add(brick_instance)
    else:
        session.merge(brick_instance)
    if commit:
        session.commit()

    return brick_instance

def fetch_brick(url, commit=True, session=None):
    from sessions import session as default_session
    if session is None:
        session = default_session

    datas = parse(url)
    for data in datas:
        yield update_brick(data, commit, session)




    


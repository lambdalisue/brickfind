# vim: set fileencoding=utf8:
"""
brickfind.db model module

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
from string import maketrans
from datetime import datetime
from sqlalchemy import event, Column, Table
from sqlalchemy import Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from .utils import get_or_create_model

Base = declarative_base()

abct = Table('association_brick_category', Base.metadata,
        Column('brick_id', Integer, ForeignKey('bricks.id'), primary_key=True),
        Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True))

class Category(Base):
    """brickfind brick category model"""
    __tablename__ = 'categories'

    DELIMITER = '/'

    id = Column(Integer, primary_key=True)
    label = Column(String(140))
    # Self-relation
    parent_id = Column(Integer, ForeignKey('categories.id'))
    children = relationship('Category', 
            backref=backref('parent', remote_side=[id]))
    # Relation
    bricks = relationship('Brick', secondary=abct, backref='categories')

    @classmethod
    def find(cls, cpath, session=None):
        from sessions import session as default_session
        session = session or default_session
        
        def _find(cpath, parent, session):
            if cls.DELIMITER in cpath:
                lhs, rhs = cpath.split(cls.DELIMITER, 1)
                dict_info = {
                    'label': lhs,
                    'parent': parent
                }
                p, created = get_or_create_model(cls, dict_info, session)
                if created:
                    session.add(p)
                    session.flush()
                return _find(rhs, p, session)
            else:
                dict_info = {
                    'label': cpath,
                    'parent': parent
                }
                return get_or_create_model(cls, dict_info, session)[0]
        # Truncate first 2 letters
        cpath = cpath[2:]
        return _find(cpath, None, session)

    @property
    def cpath(self):
        lhs = self.parent.cpath if self.parent else self.DELIMITER
        rhs = self.label
        return "%s%s%s" % (lhs, self.DELIMITER, rhs)
    @cpath.setter
    def cpath(self, value):
        lhs, rhs = value.rsplit(self.DELIMITER, 1)
        self.label = rhs
        self.parent = None if lhs == self.DELIMITER else Category.find(lhs)

    def __repr__(self):
        return "<Category (%r)>" % self.label

class Feature(Base):
    """brickfind brick feature model class"""
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    type = Column(String(20))
    direction = Column(String(20))
    startpos = Column(Integer)
    endpos = Column(Integer)

    brick_id = Column(Integer, ForeignKey('bricks.id'))
    brick = relationship("Brick", backref=backref('features', order_by=title))

    def __repr__(self):
        return "<Feature (%r)>" % self.type

class Sequence(Base):
    """brickfind brick sequence model class"""
    __tablename__ = 'sequences'

    id = Column(Integer, primary_key=True)
    _forward = Column(Text)
    _reverse = Column(Text)

    brick_id = Column(Integer, ForeignKey('bricks.id'))
    brick = relationship("Brick", backref=backref('sequences', order_by=id))

    @hybrid_property
    def sequence(self):
        return self._forward
    @sequence.setter
    def sequence(self, value):
        self._forward = value
        self._reverse = value.translate(maketrans('atgc', 'tacg'))
    @hybrid_property
    def complement(self):
        return self._reverse
    @complement.setter
    def complement(self, value):
        self._reverse = value
        self._forward = value.translate(maketrans('atgc', 'tacg'))

    def __repr__(self):
        return "<Sequence (%d bp)>" % len(self.forward)

class Brick(Base):
    """brickfind brick model class"""
    __tablename__ = 'bricks'

    id = Column(Integer, primary_key=True)
    name = Column(String(140), unique=True)
    nickname = Column(String(140))
    description = Column(Text)
    type = Column(String(20))
    status = Column(String(20))
    results = Column(String(20))
    rating = Column(Integer)
    url = Column(String(140))
    publish_at = Column(Date)
    author = Column(String(140))
    quality = Column(String(20))
    # Automatically update by event listner
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    @classmethod
    def factory(cls, data, session=None):
        from sessions import session as default_session
        session = session or default_session

        # copy data
        _data = dict(data)

        sequence = None
        if 'sequences' in _data:
            sequences = _data.pop('sequences')
        features = None
        if 'features' in _data:
            features = _data.pop('features')
        categories = None
        if 'categories' in _data:
            categories = _data.pop('categories')

        # name field is unique
        brick_query = session.query(Brick).filter_by(name=data['name'])
        brick_instance = brick_query.first()

        if not brick_instance:
            brick_instance = cls(**_data)
        else:
            # Update the instance
            brick_query.update(_data)
            # Remove all sequences and features
            if sequences:
                session.query(Sequence).filter_by(brick_id=brick_instance.id).delete()
            if features:
                session.query(Feature).filter_by(brick_id=brick_instance.id).delete()
            # Remove all association_brick_category records
            if categories:
                c = session.connection()
                c.execute(abct.delete().where(abct.c.brick_id==brick_instance.id))

        # Add sequences and features
        if sequences:
            for seq in sequences:
                sequence = Sequence(sequence=seq)
                brick_instance.sequences.append(sequence)
        if features:
            for fet in features:
                feature = Feature(**fet)
                brick_instance.features.append(feature)
        if categories:
            for cat in categories:
                category = Category.find(cpath=cat, session=session)
                brick_instance.categories.append(category)

        return brick_instance, brick_instance.id is None


    def __repr__(self):
        return "<Brick (%r)>" % self.name

# Add before_insert and before_update event to Brick
def auto_created_at_listener(mapper, connection, target):
    """Automatically set datetime.now to created_at field"""
    target.created_at = datetime.now()
def auto_updated_at_listener(mapper, connection, target):
    """Automatically set datetime.now to updated_at field"""
    target.updated_at = datetime.now()
event.listen(Brick, 'before_insert', auto_created_at_listener)
event.listen(Brick, 'before_update', auto_updated_at_listener)

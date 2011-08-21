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
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AutoTimeRecordExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.created_at = datetime.now()
    def before_update(self, mapper, connection, instance):
        instance.updated_at = datetime.now()

association_brick_category_table = Table('brick_category_association',
        Base.metadata,
        Column('brick_id', Integer, ForeignKey('bricks.id')),
        Column('category_id', Integer, ForeignKey('categories.id')))

class Brick(Base):
    """brickfind brick model class"""
    __tablename__ = 'bricks'
    __mapper_args__ = {'extension': AutoTimeRecordExtension()}

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    nickname = Column(String)
    description = Column(Text)
    type = Column(String)
    status = Column(String)
    results = Column(String)
    rating = Column(Integer)
    url = Column(String)
    publish_at = Column(Date)
    author = Column(String)
    quality = Column(String)
    # Automatically update via extension
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return "<Brick (%r)>" % self.name

class Feature(Base):
    """brickfind brick feature model class"""
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    direction = Column(String)
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
    sequence = Column(Text)

    brick_id = Column(Integer, ForeignKey('bricks.id'))
    brick = relationship("Brick", backref=backref('sequences', order_by=id))

    def __repr__(self):
        return "<Sequence (%d bp)>" % len(self.sequence)

class Category(Base):
    """brickfind brick category model class"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    label = Column(String)

    parent_id = Column(Integer, ForeignKey('categories.id'))
    children = relationship("Category", 
            backref=backref('parent', remote_side=[id]))

    bricks = relationship("Brick",
            secondary=association_brick_category_table,
            backref='categories')

    def __repr__(self):
        return "<Category (%r)>" % self.get_full_label()
    
    def get_full_label(self):
        def get_label(category):
            if category.parent:
                parent_label = get_label(category.parent)
                return "%s/%s" % (parent_label, category.label)
            else:
                return category.label
        return get_label(self)


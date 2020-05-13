'''
Created on 2014. 6. 27.

@author: lsh
'''
from datetime import datetime
from sqlalchemy import TIMESTAMP    
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Root(Base):
    __tablename__='crawler_root'
    
    id = Column(Integer, Sequence('crawler_root_id_seq'), primary_key=True)
    url = Column(String, nullable=False, unique=True)
    hit_count = Column(Integer, nullable=False)

    def __init__(self, url, hit_count=0):
        self.url = url
        self.hit_count = hit_count
        
    def __repr__(self):
        return "<Root('%s', '%s', '%s')>" % (self.id, self.url, self.hit_count)
    
class Seed(Base):
    __tablename__='crawler_seed'
    
    id = Column(Integer, Sequence('crawler_seed_id_seq'), primary_key=True)
    url = Column(String, nullable=False, unique=True)
    hit_count = Column(Integer, nullable=False)
    root_id = Column(Integer, ForeignKey("crawler_seed.root_id"))

    def __init__(self, url, root_id, hit_count=0):
        self.url = url
        self.hit_count = hit_count
        self.root_id = root_id
        
    def __repr__(self):
        return "<Seed('%s', '%s', '%s', '%s')>" % (self.id, self.url, self.hit_count, self.root_id)
    
class CrawledKnowledgeDocument(Base):
    __tablename__='crawler_crawledknowledgedocument'
    
    id = Column(Integer, Sequence('crawler_crawledknowledgedocument_id_seq'), primary_key=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_knowledge.id"))
    url = Column(String, nullable=False)
    title = Column(String(80), nullable=False)
    content  = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now())

    def __init__(self, knowledge_id, url, title, content, created_date=datetime.now()):
        self.knowledge_id = knowledge_id
        self.url = url
        self.title = title
        self.content = content
        self.created_date = created_date
        
    def __repr__(self):
        return "<CrawledKnowledgeDocument('%s', '%s', '%s', '%s', '%s')>" % \
             (self.id, self.knowledge_id, self.url, self.title, self.content)
    
class WithoutKnowledgeDocument(Base):
    __tablename__='crawler_withoutknowledgedocument'
    
    id = Column(Integer, Sequence('crawler_withoutknowledgedocument_id_seq'), primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String(80), nullable=False)
    content  = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now())
    
    def __init__(self, url, title, content):
        self.url = url
        self.title = title
        self.content = content
        
    def __repr__(self):
        return "<withoutknowledgedocument('%s', '%s', '%s', '%s')>" % (self.id, self.url, self.title, self.content)

class CurrentSearchKeyword(Base):
    __tablename__='crawler_currentsearchkeyword'
    
    id = Column(Integer, Sequence('crawler_currentsearchkeyword_id_seq'), primary_key=True)
    keyword  = Column(String(80), nullable=False, unique=True)
    
    def __init__(self, keyword):
        self.keyword = keyword
        
    def __repr__(self):
        return "<currentsearchkeyword('%s', '%s')>" % (self.id, self.keyword)
    
class CandidateSearchKeyword(Base):
    __tablename__='crawler_candidatesearchkeyword'
    
    id = Column(Integer, Sequence('crawler_candidatesearchkeyword_id_seq'), primary_key=True)
    keyword  = Column(String(80), nullable=False, unique=True)
    
    def __init__(self, keyword):
        self.keyword = keyword
        
    def __repr__(self):
        return "<candidatekeyword('%s', '%s')>" % (self.id, self.keyword)

class Morpheme(Base):
    __tablename__='crawler_morpheme'
    
    id = Column(Integer, Sequence('crawler_morpheme_id_seq'), primary_key=True)
    morpheme = Column(String(50), nullable=False, unique=True)
    weight_value = Column(Integer)
    
    def __init__(self, morpheme, weight_value):
        self.morpheme = morpheme
        self.weight_value = weight_value
        
    def __repr__(self):
        return "<Morpheme('%s', '%s', '%s')>" % (self.id, self.morpheme, self.weight_value)

#knowledge models
class Category(Base):
    __tablename__='knowledge_category'
    
    id = Column(Integer, Sequence('knowledge_category_id_seq'), primary_key=True)
    category_name = Column(String(40), nullable=False, unique=True)

    def __init__(self, category_name):
        self.category_name = category_name
        
    def __repr__(self):
        return "<Category('%s', '%s')>" % (self.id, self.category_name)

class Knowledge(Base):
    __tablename__='knowledge_knowledge'
    
    id = Column(Integer, Sequence('knowledge_knowledge_id_seq'), primary_key=True)
    category_id = Column(Integer, ForeignKey("knowledge_category.id"))
    knowledge_name = Column(String(50), nullable=False, unique=True)

    def __init__(self, category_id, knowledge_name):
        self.category_id = category_id
        self.knowledge_name = knowledge_name
        
    def __repr__(self):
        return "<Knowledge('%s', '%s', '%s')>" % (self.id, self.category_id, self.knowledge_name)
    
class KnowledgeAssociation(Base):
    __tablename__='knowledge_knowledge_associated_knowledge'
    
    id = Column(Integer, Sequence('knowledge_knowledge_associated_knowledge_id_seq'), primary_key=True)
    from_knowledge_id = Column(Integer, ForeignKey("knowledge_knowledge.id"))
    to_knowledge_id  = Column(Integer, ForeignKey("knowledge_knowledge.id"))

    def __init__(self, from_knowledge_id, to_knowledge_id):
        self.from_knowledge_id = from_knowledge_id
        self.to_knowledge_id = to_knowledge_id
        
    def __repr__(self):
        return "<Knowledge('%s', '%s', '%s')>" % (self.id, self.from_knowledge_id, self.to_knowledge_id)
    



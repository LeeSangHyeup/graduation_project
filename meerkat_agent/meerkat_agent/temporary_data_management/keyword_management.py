#-*- coding: utf-8 -*-
'''
Created on 2014. 6. 23.

@author: lsh
'''

import os
import time
from bsddb3 import db
from sqlalchemy.orm import sessionmaker

#meerkat modules
from global_objects import DB_ENGINE
from models.db_server import Knowledge
from models.db_server import CandidateSearchKeyword
from models.db_server import CurrentSearchKeyword
from models.db_server import Morpheme


class KeywordManager(object):
    '''
    classdocs
    '''
    
    _candidate_search_keyword_db_name = 'candidate_search_keyword_db'
    _candidate_search_keyword_db = None
    _candidate_search_keyword_index = 0
    
    _crawled_search_keyword_db_name = 'crawled_search_keyword_db'
    _crawled_search_keyword_db = None
    
    _morpheme_db_name = 'morpheme_db'
    _morpheme_db = None

    def __init__(self):
        '''
        Constructor
        '''

        self._candidate_search_keyword_db = db.DB()
        #queue max size of BerkeleyDB is 4067
        self._candidate_search_keyword_db.set_re_len(4067)
        self._candidate_search_keyword_db.open(
           self._candidate_search_keyword_db_name, None, db.DB_QUEUE, db.DB_CREATE)
        
        self._crawled_search_keyword_db = db.DB()
        self._crawled_search_keyword_db.open(
           self._crawled_search_keyword_db_name, None, db.DB_HASH, db.DB_CREATE)
        
        self._morpheme_db = db.DB()
        self._morpheme_db.open(self._morpheme_db_name, None, db.DB_HASH, db.DB_CREATE)
    
    def __del__(self):
        pass
    
    def clean_all_db(self):
        self._candidate_search_keyword_db.close()
        self._crawled_search_keyword_db.close()
        self._morpheme_db.close()
        
        os.remove(self._candidate_search_keyword_db_name)
        os.remove(self._crawled_search_keyword_db_name)
        os.remove(self._morpheme_db_name)
        
    def init_db(self):
        self._load_crawled_search_keyword()
        self._load_morpheme()
        
        self._candidate_search_keyword_db.close()
        self._crawled_search_keyword_db .close()
        self._morpheme_db.close()
    
    def _load_morpheme(self):
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()

        morphemes = session.query(Morpheme).all()
        
        session.close()
        
        for morpheme in morphemes:
            self._add_morpheme(morpheme)

    def _add_morpheme(self, morpheme):
        self._morpheme_db.put(
          str(morpheme.morpheme.encode('utf-8')), str(morpheme.weight_value))
        
    def _load_crawled_search_keyword(self):
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()
        
        knowledge_names = session.query(Knowledge.knowledge_name).all()

        for knowledge_name in knowledge_names:
            self.add_crawled_search_keyword(knowledge_name[0].encode('utf-8'))
            
        candidate_search_keywords = session.query(CandidateSearchKeyword).all()

        for candidate_search_keyword in candidate_search_keywords:
            self.add_crawled_search_keyword(candidate_search_keyword.keyword.encode('utf-8'))

        current_search_keywords = session.query(CurrentSearchKeyword.keyword).all()
        
        session.close()
        
        for current_search_keyword in current_search_keywords:
            self.add_crawled_search_keyword(current_search_keyword.keyword.encode('utf-8'))
            
    def add_crawled_search_keyword(self, search_keyword):
        self._crawled_search_keyword_db.put(
            str(search_keyword), 'NEVER_USED')
        
    def add_candidate_search_keyword(self, search_keyword):
        self._candidate_search_keyword_index += 1
        self._candidate_search_keyword_db.put(
            self._candidate_search_keyword_index, str(search_keyword))
        
    def pull_candidate_keyword(self):
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()
        
        is_query_success = False
        while not is_query_success:
            candidate_keyword_model = session.query(CandidateSearchKeyword).order_by('id').first()
            
            if candidate_keyword_model is None: 
                time.sleep(1)
                continue
            
            is_query_success = True
                    
        candidate_keyword = candidate_keyword_model.keyword.encode('utf-8')
        session.add(CurrentSearchKeyword(candidate_keyword))
        self.add_crawled_search_keyword(candidate_keyword)
        
        session.delete(candidate_keyword_model)
        session.commit()
        
        session.close()
        
        return candidate_keyword
    
    def delete_current_search_keyword(self, keyword):
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()
        
        session.query(CurrentSearchKeyword).filter_by(keyword=keyword).delete()
        session.commit()
        
        session.close()
    
    def check_crawled_keyword_exist(self, keyword):
        return self._crawled_search_keyword_db.has_key(keyword)
    
    def check_morpheme_exist(self, morpheme):
        return self._morpheme_db.has_key(morpheme)
    
    def inquiry_morpheme(self, keyword):
        return self._morpheme_db.get(keyword)

    def store_candidate_search_keyword(self):
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()

        cursor = self._candidate_search_keyword_db.cursor()
        row = cursor.first()
        
        while row:
            new_candidate_search_keyword = CandidateSearchKeyword(row[1].strip())
            
            session.add(new_candidate_search_keyword)
            
            try:
                session.commit()
            except:
                pass
            
            row = cursor.next()
            
        session.close()
        
        




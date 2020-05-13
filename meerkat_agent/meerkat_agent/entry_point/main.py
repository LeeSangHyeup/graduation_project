#-*- coding: utf-8 -*-
'''
Created on 2014. 6. 23.

@author: lsh
'''
import gc
from sqlalchemy.orm import sessionmaker

#meerkat modules
from global_objects import CONFIG
from global_objects import DB_ENGINE
from crawler.crawler import Crawler
from pathfinder.pathfinder import Pathfinder
from models.db_server import Knowledge
from models.db_server import Category
from inside_document_collecter.inside_document_collecter import InsideDocumentCollector
from temporary_data_management.keyword_management import KeywordManager

def correct_document():
    while True:
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()

        keyword_manager = KeywordManager()
    
        search_keyword = keyword_manager.pull_candidate_keyword()
        print 'Searchkeyword = ' + search_keyword
        
        category = session.query(Category).filter_by(category_name=CONFIG.CATEGORY).first()

        knowledge = session.query(Knowledge).filter_by(knowledge_name=search_keyword).first()
        if knowledge is None:
            knowledge = Knowledge(category.id, search_keyword)
            session.add(knowledge)
            session.commit()
            
        knowledge = session.query(Knowledge).filter_by(knowledge_name=search_keyword).first()
        session.close()
        
        inside_document_corrector = InsideDocumentCollector(search_keyword)
        print '\ncollecting from crawled_knowledge_docuemnts..'
        correct_document_count = inside_document_corrector.collect_document_from_crawled_knowledge_document(knowledge)
        print 'finish. collected '+str(correct_document_count)
        

        print '\ncollecting from without_knowledge_docuemnts..'
        correct_document_count += inside_document_corrector.collect_document_from_without_knowledge_document(knowledge)
        print 'finish. collected '+str(correct_document_count)
        

        print '\ncollecting from web..'
        correct_document_count += Crawler().collect_document_from_web(
         search_keyword, knowledge)
        print 'finish. collected '+str(correct_document_count)
        
        if correct_document_count < 1:
            Session = sessionmaker(bind=DB_ENGINE)
            session = Session()
            session.delete(knowledge)
            session.commit()
            session.close()
            continue
        
        print '\ncreating knowledge association..'
        # 지식관계설정
        pathfinder = Pathfinder()
        pathfinder.find_path(knowledge)
        print 'done.\n'
        
        keyword_manager.delete_current_search_keyword(search_keyword)
        
        #call garbage collector
        gc.enable()

if __name__ == '__main__':
    correct_document()
    

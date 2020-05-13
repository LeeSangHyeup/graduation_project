#-*- coding: utf-8 -*-
'''
Created on 2014. 6. 23.

@author: lsh
'''

from sqlalchemy.orm import sessionmaker

#meerkat modules
from suitability_checker.suitability_checker import SuitabilityChecker
from morpheme_analyzer.morpheme_analyzer import MorphemeAnalyzer
from models.db_server import Knowledge
from models.db_server import CrawledKnowledgeDocument
from models.db_server import WithoutKnowledgeDocument
from global_objects import DB_ENGINE

class _StealedKnowledge:
    def __init__(self, knowledge_name, stealed_count):
        self.knowledge_name = knowledge_name
        self.stealed_count = stealed_count

class InsideDocumentCollector(object):
    '''
    collect document from dbserver
    '''
    
    _search_keyword = None
    
    _morpheme_analyzer = MorphemeAnalyzer()
    
    _suitability_checker = SuitabilityChecker()

    def __init__(self, search_keyword):
        '''
        Constructor
        '''
        
        self._search_keyword = search_keyword
    
    def collect_document_from_crawled_knowledge_document(self, knowledge):
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()
        
        knowledges = session.query(Knowledge).all()

        stealed_knowledge_list = []
            
        for knowledge in knowledges:
            crawled_knowledge_documents = session.query(
                CrawledKnowledgeDocument).filter_by(knowledge_id=knowledge.id).all()

            for crawled_knowledge_document in crawled_knowledge_documents:
                morpheme_list = self._morpheme_analyzer.analyze_morpheme(
                    crawled_knowledge_document.content.encode('utf-8'))
                is_keyword_correlation = self._suitability_checker.check_keyword_correlation(
                    self._search_keyword, morpheme_list)
               
                if not is_keyword_correlation:
                    continue

                keyword_rank = self._morpheme_analyzer.calculate_rank(self._search_keyword, morpheme_list)
                each_document_keyword_rank = self._morpheme_analyzer.calculate_rank(
                    knowledge.knowledge_name.encode('utf-8'), morpheme_list)

                if keyword_rank <= each_document_keyword_rank:
                    continue

                self.count_stealed(knowledge, stealed_knowledge_list)

                session.query(CrawledKnowledgeDocument).filter(
                   CrawledKnowledgeDocument.id==crawled_knowledge_document.id).update({'knowledge_id':knowledge.id})
                session.commit()
                
        session.close()
                
        correct_document_count = len(stealed_knowledge_list)

        return correct_document_count

    def collect_document_from_without_knowledge_document(self, knowledge):
        # 웹에서 수집된 문서에 대해 수행
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()
            
        without_knowledge_documents = session.query(WithoutKnowledgeDocument).all()

        correct_document_count = 0

        for without_knowledge_document in without_knowledge_documents:
            morpheme_list = self._morpheme_analyzer.analyze_morpheme(without_knowledge_document.content.encode('utf-8'))
            is_keyword_correlation = self._suitability_checker.check_keyword_correlation(self._search_keyword, morpheme_list)
           
            if not is_keyword_correlation:
                continue
            
            url = without_knowledge_document.url
            title = without_knowledge_document.title
            content = without_knowledge_document.content
            created_date = without_knowledge_document.created_date

            new_crawled_knowledge_document = CrawledKnowledgeDocument(knowledge.id, url, title, content, created_date)
            
            session.add(new_crawled_knowledge_document)
            session.delete(without_knowledge_document)
            session.commit()
            
            correct_document_count += 1
            
        session.close()
        
        return correct_document_count
        
    def count_stealed(self, knowledge, stealed_knowledge_list):
        # same_knowledge_list에 추가하려는 객체가 이미 존재하는지 검사
            same_knowledge_list = [x for x in stealed_knowledge_list if x.knowledge_name == knowledge.knowledge_name]
            same_knowledge_list_length = len(same_knowledge_list)
            assert (same_knowledge_list_length == 0) or (same_knowledge_list_length == 1), 'same_knowledge_list에 중복값이 존재합니다.'
            
            # 새 요소 추가
            if same_knowledge_list_length == 0 : 
                stealed_knowledge_list.append(_StealedKnowledge(knowledge.knowledge_name, 1))
            # 기존 요소에 값 추가
            else:
                same_knowledge_list[0].stealed_count += 1
                
            return True
    
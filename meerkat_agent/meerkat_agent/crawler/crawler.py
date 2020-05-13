# -*- coding: utf-8 -*-
'''
Created on 2014. 4. 24.

@author: lee sang hyeop
'''
import xmlrpclib
import multiprocessing
from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Value
from sqlalchemy.orm import sessionmaker

#meerkat modules
from global_objects import CONFIG
from global_objects import DB_ENGINE
from morpheme_analyzer.morpheme_analyzer import MorphemeAnalyzer
from morpheme_analyzer.morpheme_analyzer import Morpheme
from suitability_checker.suitability_checker import SuitabilityChecker
from html_extractor import HtmlExtractor
from temporary_data_management.keyword_management import KeywordManager
from models.db_server import WithoutKnowledgeDocument
from models.db_server import CrawledKnowledgeDocument
from models.xmlrpc import CandidateUrl
from models.xmlrpc import Seed

class Crawler:
    '''
    웹문서 수집
    '''
    
    _morpheme_analyzer = MorphemeAnalyzer()

    _suitability_checker = SuitabilityChecker()
    
    _search_page_count = Value('i', 0)
    
    _collect_document_count = Value('i', 0)
    
    _manager = Manager()
    
    _candidate_url_list = _manager.list()
    
    _candidate_seed_list = _manager.list()
    
    _without_knowledge_documents = _manager.list()
    
    _crawled_knowledge_documents = _manager.list()
    
    _stuck_process_quantity = Value('i', 0)
    
    _process_quantity = Value('i', multiprocessing.cpu_count() * CONFIG.CRAWLER_PROCESS_WEIGHTVALUE)
    
    def __init__(self):
        pass

    def collect_document_from_web(self, search_keyword, knowledge):
        self._collect_document_count.value = 0
        self._search_page_count.value = 0
        keyword_manager = KeywordManager()
        keyword_manager.init_db()
        
        proxy = xmlrpclib.ServerProxy('http://'+CONFIG.URL_SERVER_HOST+':'+CONFIG.URL_SERVER_PORT)
        candidate_url_dictionary = proxy.request_candidate_url()
        for candidate_url in candidate_url_dictionary:
            url = candidate_url['url']
            seed_url =candidate_url['seed_url']
            self._candidate_url_list.append(CandidateUrl(url, seed_url))
        
        # cpu 코어 개수, 코어개수*프로세스가중치 만큼 프로세스를 생성하여 검색수행.
        process_list = []
        for NEVER_USED in range(self._process_quantity.value):
            new_process = Process(target=self.collect_document_from_web_process,
              args=(search_keyword, knowledge))
            process_list.append(new_process)
            
        for each_process in process_list:
            each_process.start()
            
        for each_process in process_list:
            each_process.join()

        KeywordManager().store_candidate_search_keyword()
        self._store_seed()
            
        if self._collect_document_count.value >= 1:
            self._store_crawled_knowledge_document()

        keyword_manager.clean_all_db()
        
        return self._collect_document_count.value
           
    def collect_document_from_web_process(self, search_keyword, knowledge):
        while True:
            if len(self._candidate_url_list)<=0:
                return True
            
            current_candidate_url = self._candidate_url_list.pop(0)
            crawling_url = current_candidate_url.url
            print multiprocessing.current_process().name + '-' + crawling_url
               
            try:
                html_extractor = HtmlExtractor(crawling_url)
            except:
                continue
            
            title = html_extractor.extract_title()

            # url에서 본문추출, 일부 페이지에서 goose가 작동중에 UnicodeDecodeError가 발생하여 임시로 except로 막아둠. 여유되면 자세히 알아볼 것.
            try:
                article = html_extractor.extract_main_text()
            except Exception:
                continue
            
            # 추출된 본문의 내용이 적어 지식문서로서의 가치가 없으면 해당 html페이지를 무시함    
            if len(article.strip()) < 100:
                continue
                
            # 본문의 형태소를 분석
            morpheme_list = self._morpheme_analyzer.analyze_morpheme(article)
            
            # 본문의 적합성 검사
            if not self._suitability_checker.check_article_suitability(morpheme_list):
                continue
            
            self._candidate_seed_list.append(current_candidate_url)
            
            # 키워드와 분문 연관성 검사
            if not self._suitability_checker.check_keyword_correlation(search_keyword, morpheme_list):
                self._without_knowledge_documents.append(WithoutKnowledgeDocument(
                  crawling_url, title, article))
                continue
            
            # 다음 검색을 위한 후보 키워드를 추출하여 db에 저장
            self.correct_candidate_search_keyword(search_keyword, morpheme_list)

            # 검색된 문서 리스트에 임시저장
            new_crawled_knowledge_document = CrawledKnowledgeDocument(
              knowledge.id, crawling_url, title, article)
            self._crawled_knowledge_documents.append(new_crawled_knowledge_document)

            self._collect_document_count.value += 1
            print 'found %d documents' % (self._collect_document_count.value)
            
        return True
        
    def correct_candidate_search_keyword(self, current_search_keyword, morpheme_list):
        keyword_manager = KeywordManager()
        candidate_keywords = []
        for morpheme in morpheme_list:
            
            pure_korean_alphabet_morpheme = self._morpheme_analyzer.extract_korean_alphabet(morpheme.morpheme)
            
            # 형태소가 한글이 아니면 키워드로 인정하지 않음
            if pure_korean_alphabet_morpheme == None:
                continue
            
            #2글자 미만이면 키워드로 인정하지 않음
            if len(pure_korean_alphabet_morpheme)<6:
                continue
            
            # 현재 검색중인 키워드와 같으면 수집하지 않음
            if pure_korean_alphabet_morpheme == current_search_keyword:
                continue

            if keyword_manager.check_crawled_keyword_exist(pure_korean_alphabet_morpheme):
                continue

            candidate_keywords.append(Morpheme(pure_korean_alphabet_morpheme, morpheme.rank, morpheme.frequency))
            
        if len(candidate_keywords)==0:
            return False
        
        candidate_keywords.sort(key=lambda x: x.rank)

        most_frequently_morpheme = candidate_keywords[0]
        keyword_manager.add_candidate_search_keyword(most_frequently_morpheme.morpheme)
        keyword_manager.add_crawled_search_keyword(most_frequently_morpheme.morpheme)
        
        return True
    
    def _store_crawled_knowledge_document(self):
        count = 0

        for crawled_knowledge_document in self._crawled_knowledge_documents:
            new_crawled_knowledge_document = CrawledKnowledgeDocument(
               knowledge_id=crawled_knowledge_document.knowledge_id,
               url=crawled_knowledge_document.url,
               title=crawled_knowledge_document.title,
               content=crawled_knowledge_document.content,
                                )
            Session = sessionmaker(bind=DB_ENGINE)
            session = Session()
            
            session.add(new_crawled_knowledge_document)
            
            session.commit()
            session.close()
            count+=1
            
        for without_knowledge_document in self._without_knowledge_documents:
            new_without_knowledge_document = WithoutKnowledgeDocument(
               url=without_knowledge_document.url,
               title=without_knowledge_document.title,
               content=without_knowledge_document.content,
                                )
            Session = sessionmaker(bind=DB_ENGINE)
            session = Session()
            
            session.add(new_without_knowledge_document)
            
            session.commit()
            session.close()
            Session.close_all()
            count+=1
        
    def _store_seed(self):
        seed_list = []
        for candidate_seed in self._candidate_seed_list:
            new_seed = Seed(candidate_seed.url, candidate_seed.seed_url)
            seed_list.append(new_seed)
            
        proxy = xmlrpclib.ServerProxy('http://'+CONFIG.URL_SERVER_HOST+':'+CONFIG.URL_SERVER_PORT)
        proxy.store_seed(seed_list)
        
        
        
        

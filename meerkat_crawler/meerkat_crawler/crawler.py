'''
Created on 2014. 8. 27.

@author: lsh
'''

import xmlrpclib
import logging
from multiprocessing import Process
from multiprocessing import Queue
from time import sleep
from os import path
from os import remove

#exception's
from Queue import Empty
from urllib2 import HTTPError
from urllib2 import URLError
from socket import timeout

#meerkat modules
from config import CONFIG
from models.xmlrpc import Document
from html_extractor import HtmlExtractor
from suitability_checker.baysian_classifier import KoreanHistoryClassifier
from master_keyword_extractor import MasterKeywordExtractor


class Crawler:

    def __init__(self):
        self._candidate_url_queue = Queue()
        
        self._korean_history_classifier = KoreanHistoryClassifier()
        
        self._url_server_proxy = xmlrpclib.ServerProxy(
           'http://'+CONFIG.URL_SERVER_IP+':'+str(CONFIG.URL_SERVER_PORT))
        self._document_server_proxy = xmlrpclib.ServerProxy(
           'http://'+CONFIG.DOCUMENT_SERVER_IP+':'+str(CONFIG.DOCUMENT_SERVER_PORT))
        
        self._temporary_data_path = 'temporary_data/'
        
        self._temporary_url_file_name = 'temporary_url.txt'
        
        self._temporary_url_file_path = self._temporary_data_path + self._temporary_url_file_name
        
        self._ignore_url_desinences = ['png', 'jpg', 'gif']
        
    def __del__(self):
        with open(self._temporary_url_file_path, 'w') as temporary_url_file:
            while True:
                try:
                    temporary_url = self._candidate_url_queue.get_nowait()
                    temporary_url_file.write(temporary_url+'\n')
                except Empty:
                    break
        
    def collect_document(self):
        while True:
            assert self._candidate_url_queue.empty(), "can't start new crawl candidate url still remain"
            
            if path.isfile(self._temporary_url_file_path):
                with open(self._temporary_url_file_path, 'r') as temporary_url_file:
                    for line in temporary_url_file:
                        self._candidate_url_queue.put(line.strip())
                        
                remove(self._temporary_url_file_path)
                
            else:
                request_urls = self._url_server_proxy.request_candidate_url(CONFIG.URL_REQUEST_QUANTITY)
                if request_urls==False:
                    print 'not enough candidate_url'
                    sleep(1)
                    continue
                    
                assert len(set(request_urls)) == CONFIG.URL_REQUEST_QUANTITY, 'duplication url exist'
                
                for request_url in request_urls:
                    self._candidate_url_queue.put(request_url)
            
            process_list = []
            for NEVER_USED in range(CONFIG.CRAWLER_PROCESS_QUANTITY):
                new_process = Process(target=self._collect_document_process)
                process_list.append(new_process)
                new_process.start()
                
            for process in process_list:
                process.join()
        
    def _collect_document_process(self):
        while True:
            try:
                target_url = self._candidate_url_queue.get_nowait()
            except Empty:
                return
            
            for self._ignore_url_desinence in self._ignore_url_desinences:
                if target_url.endswith(self._ignore_url_desinence):
                    continue
            
            try:
                html_extractor = HtmlExtractor(target_url)
            #except (HTTPError, EOFError, timeout, URLError), e:
            except Exception, e:
                logging.exception('Exception raised in method _collect_document_process with url='+target_url)
                continue
                
            document_content = html_extractor.extract_main_text()
            
            if document_content==None:
                continue
            
            if len(document_content) < 500:
                continue 
            
            is_article_suitable = self._korean_history_classifier.binary_classify(document_content)
            if not is_article_suitable:
                continue
            
            document_url = target_url
            document_title = html_extractor.extract_title()
            if ':' in document_title:
                continue
            
            title_terms = document_title.split()
            
            if len(title_terms)==1:
                document_topic = document_title
            else:
                document_topic = MasterKeywordExtractor().extract_master_keyword(document_title, document_content)
            
            if document_topic == None:
                continue
            
            new_document = Document(
                document_topic, document_url, document_title, document_content)
   
            self._document_server_proxy.store_crawled_knowledge_document(new_document, CONFIG.CATEGORY)
            print 'document ' + document_title + ' is  stored ' + 'with topic ' + document_topic
        
#-*- coding: utf-8 -*-
'''
Created on 2014. 6. 21.

@author: lsh
'''

import logging
import urllib2
import urlparse
from goose import Goose
from goose.text import StopWordsKorean

class HtmlExtractor(object):
    '''
    classdocs
    '''
    #추출을 수행할 html코드
    _target_html_code = None
    _target_url = None

    def __init__(self, url):
        '''
        Constructor
        '''

        try:
            response_from_url = urllib2.urlopen(url, timeout=5)
        except:
            raise
        
        try:
            self._target_html_code = response_from_url.read()
        except:
            raise
        
        self._target_url = urlparse.urlparse(url)
    
    def extract_title(self):
        '''
        extract content in title tag from attribute _target_html_code
        '''
        target_domain = self._target_url.hostname
        if target_domain=='ko.wikipedia.org':
            return self._extract_wikipedia_title()
        elif target_domain=='terms.naver.com':
            return self._extract_naver_dict_title()
        elif target_domain=='mirror.enha.kr':
            return self._extract_enha_title()
        else:
            assert False, "invalid domain_name '"+target_domain+"'"
        
    def extract_main_text(self):
        '''
        extract main text from attribute _target_html_code
        '''

        gooseExtractor = Goose({'stopwords_class':StopWordsKorean, 'parser_class':'lxml',
                                     'enable_image_fetching' : False})
        
        url = self._target_url.geturl()
        try:
            main_text = gooseExtractor.extract(url).cleaned_text.encode('utf8')
        except Exception, e:
            print str(e), url
            logging.exception('Exception raised in method extract_main_text with url='+url)
            return None
            
        return main_text  

    def _extract_pure_title(self, remove_string):
        start_position = self._target_html_code.find('<title>')
        
        if start_position != -1:
            endPos = self._target_html_code.find('</title>', start_position+7)
            if endPos != -1:
                title = self._target_html_code[start_position+7:endPos]
        
        title = title.replace(remove_string, '')
        
        return title.strip()
        
                
    def _extract_wikipedia_title(self):
        return self._extract_pure_title(' - 위키백과, 우리 모두의 백과사전')
                
    def _extract_naver_dict_title(self):
        return self._extract_pure_title(' : 지식백과')
        
    def _extract_enha_title(self):
        return self._extract_pure_title(' - 엔하위키 미러')
                
                
                
        
        
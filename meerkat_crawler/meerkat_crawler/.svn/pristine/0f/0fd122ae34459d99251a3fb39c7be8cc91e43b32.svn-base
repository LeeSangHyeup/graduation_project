'''
Created on 2014. 8. 28.

@author: lsh
'''

import re
import logging
from numpy import array 
from numpy import ndarray
from mdp.nodes import PCANode

#meerkat_modules
from morpheme_analyzer.morpheme_analyzer import MorphemeAnalyzer
from suitability_checker.keyword_handler import KeywordHandler


class MasterKeywordExtractor:

    def __init__(self):
        self._morpheme_analyzer = MorphemeAnalyzer()
        self._keyword_handler = KeywordHandler()
        self._PASS_CORRELATION_SCORE = 0.5
        
    def extract_master_keyword(self, title, article):
        assert article != None, 'article is invalid'
        assert len(article) > 0, 'article is invalid'
        
        title_morpheme_list = self._morpheme_analyzer.analyze_morpheme(title)
        title_keywords = [morpheme.morpheme for morpheme in title_morpheme_list]
        
        article_morpheme_list = self._morpheme_analyzer.analyze_morpheme(article)
        #article_morpheme_list = filter(lambda x:x.frequency > 1, article_morpheme_list)
        
        article_matrix = self._create_article_matrix(article, article_morpheme_list)
        
        if not isinstance(article_matrix, ndarray):
            return None
        
        pca = PCANode(svd=True)
        try:
            pca.execute(article_matrix)
        except Exception, e:
            print str(e), title
            logging.exception('Exception raised in method extract_master_keyword with article title='+title)

        topic_dict = self._extract_topics(pca, article_morpheme_list)
        master_keyword = None
        for topic_rank in range(1, len(topic_dict)+1):
            if topic_dict[topic_rank] in title_keywords:
                master_keyword = topic_dict[topic_rank]
                return master_keyword

        if len(title_morpheme_list)==0:
            return None
        
        master_keyword = title_morpheme_list[0].morpheme
        
        return master_keyword
    
    def _extract_topics(self, pca, morpheme_list):
        total_eigenvalue = sum(pca.d)
        accumulation_rates = []
        for eigenvalue in pca.d:
            if eigenvalue==0:
                continue
            
            accumulation_rate = eigenvalue / total_eigenvalue 
            
            if accumulation_rate < 1:
                accumulation_rates.append(accumulation_rate)
                
        topic_indexes = set()
        for principal_index in range(len(accumulation_rates)):
            principal = pca.v.T[principal_index].tolist()
            correlations = filter(lambda x: abs(x)>=0.5, principal)
            correlations  = [abs(correlation) for correlation in correlations]
            correlations.sort(reverse=True)
            for correlation in correlations:
                topic_index = None
                if correlation in principal:
                    topic_index=(principal.index(correlation))
                else:
                    topic_index=(principal.index(correlation * -1))

                history_inquiry_result = self._keyword_handler.\
                    inquiry_history_keyword(morpheme_list[topic_index].morpheme)
                    
                not_history_inquiry_result = self._keyword_handler.\
                    inquiry_not_history_keyword(morpheme_list[topic_index].morpheme)

                if history_inquiry_result==None and not_history_inquiry_result!=None:
                    continue
                
                elif history_inquiry_result!=None and not_history_inquiry_result!=None:
                    history_frequency = history_inquiry_result[1]
                    not_history_frequency = not_history_inquiry_result[1]
                    if not_history_frequency > 200:
                        continue
                    
                    if history_frequency <= not_history_frequency:
                        continue

                topic_indexes.add(topic_index)
                
        topics = {}
        topic_rank = 1
        for topic_index in topic_indexes:
            topic = morpheme_list[topic_index].morpheme
            topics[topic_rank] = topic
            topic_rank += 1
            
        return topics
        
    def _create_article_matrix(self, article, article_morpheme_list):
        tmp_sentences = re.split(r'[.!?]\s*', article)
        sentence_list=[]
        
        if len(tmp_sentences) < 2:
            return None
        
        for sentence in tmp_sentences:
            sentence = sentence.strip()
            if (sentence=='') or (len(sentence)==0):
                    continue
        
            vector_raw = self._create_vector_raw(sentence, article_morpheme_list)
            not_zero_elements = filter(lambda x:x!=0, vector_raw)
            if len(not_zero_elements) > 0:
                sentence_list.append(vector_raw)
                
        article_matrix = array(sentence_list)
        
        return article_matrix
        
    def _create_vector_raw(self, sentence, article_morpheme_list):
        sentence_keywords = self._morpheme_analyzer.analyze_morpheme(sentence)
    
        sentence=[]
        for keyword in article_morpheme_list:
            match_keyword = filter(lambda x:x.morpheme==keyword.morpheme, sentence_keywords)
            if len(match_keyword)==0:
                sentence.append(float(0))
            else:
                sentence.append(float(match_keyword[0].frequency))
        
        return sentence
    
    
    
    
    
    
    
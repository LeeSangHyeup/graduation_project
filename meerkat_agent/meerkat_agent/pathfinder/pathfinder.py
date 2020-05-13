#-*- coding: utf-8 -*-
'''
Created on 2014. 5. 12.

@author: lsh
'''

import math
from sqlalchemy.orm import sessionmaker

#meerkat modules
from global_objects import DB_ENGINE
from morpheme_analyzer.morpheme_analyzer import MorphemeAnalyzer
from models.db_server import Knowledge
from models.db_server import KnowledgeAssociation
from models.db_server import CrawledKnowledgeDocument


from suitability_checker.suitability_checker import SuitabilityChecker

class Pathfinder:
    '''
    classdocs
    '''
    
    _suitability_checker = SuitabilityChecker()
    _morpheme_analyzer = MorphemeAnalyzer()
    _extract_morpheme_list = None
    
    
    def __init__(self):
        '''
        Constructor
        '''

    def find_path(self, knowledge):
        Session = sessionmaker(bind=DB_ENGINE)
        session = Session()
        
        #현재 지식을 제외한 모든 지식을 조회
        comparison_target_knowledgies = session.query(Knowledge).filter(Knowledge.knowledge_name!=knowledge.knowledge_name).all()
        
        crawled_knowledge_documents = session.query(CrawledKnowledgeDocument).all()
        
        filtered_documents = self._filter_target_knowledge_document(knowledge, crawled_knowledge_documents)
        
        for comparison_target_knowledge in comparison_target_knowledgies:
            if session.query(KnowledgeAssociation).filter(KnowledgeAssociation.from_knowledge_id==knowledge.id).\
                filter(KnowledgeAssociation.to_knowledge_id==comparison_target_knowledge.id).first():
                continue
            
            comparison_filtered_documents = self._filter_target_knowledge_document(
              comparison_target_knowledge, crawled_knowledge_documents)

            similarity_score = self._compute_cosine_similarity(
               filtered_documents, comparison_filtered_documents, crawled_knowledge_documents)

            pass_score = 0.3

            if similarity_score < pass_score:
                continue 
            
            session.add(KnowledgeAssociation(knowledge.id, comparison_target_knowledge.id))
            session.commit()
            
            print '유사도 점수 = ' + str(similarity_score)
            
            print '관계생성 '+knowledge.knowledge_name.encode('utf-8')+\
                ', '+comparison_target_knowledge.knowledge_name.encode('utf-8')
            
        session.close()
        
        return True
    
    def _compute_cosine_similarity(self, filtered_documents, comparison_filtered_documents, crawled_knowledge_documents):
        vector_space_model = self._create_vector_space_model(
         filtered_documents, comparison_filtered_documents, crawled_knowledge_documents)
        
        sumxx, sumxy, sumyy = 0, 0, 0
        
        for each_dimension in vector_space_model:
            x = each_dimension[0]
            y = each_dimension[1]
            
            if x==0:
                multiplication_xx=0
            else:
                multiplication_xx=x*x
            if y==0:
                multiplication_yy=0
            else:
                multiplication_yy=y*y
            if x==0 or y==0:
                multiplication_xy=0
            else:
                multiplication_xy=x*y

            sumxx += multiplication_xx
            sumyy += multiplication_yy
            sumxy += multiplication_xy
            
        return sumxy/math.sqrt(sumxx*sumyy)
    
    def _create_vector_space_model(self, filtered_documents, comparison_filtered_documents, crawled_knowledge_documents):
        morpheme_list1 = []
        for each_document in filtered_documents:
            morpheme_list1 += self._morpheme_analyzer.analyze_morpheme(each_document.content)

        morpheme_list2 = []
        for each_document in comparison_filtered_documents:
            morpheme_list2 += self._morpheme_analyzer.analyze_morpheme(each_document.content)
        
        tfidf_dictionary1 = self._compute_normalized_tfidf(morpheme_list1, crawled_knowledge_documents)
        tfidf_dictionary2 = self._compute_normalized_tfidf(morpheme_list2, crawled_knowledge_documents)
        
        vector_space_model = []
            
        for key in tfidf_dictionary1:
            tfidf1 = tfidf_dictionary1[key]
            tfidf2 = tfidf_dictionary2[key]
            
            vector_space_model.append([tfidf1, tfidf2])
            
        return vector_space_model
    
    def _compute_normalized_tfidf(self, morpheme_list, crawled_knowledge_documents):
        document_length = 0
        for morpheme in morpheme_list:
            document_length += morpheme.frequency
        
        tfidf_dictionary = {}
        for morpheme in morpheme_list:
            document_hava_morpheme_count = 0
            
            for crawled_knowledge_document in crawled_knowledge_documents:
                if morpheme.morpheme in crawled_knowledge_document.content:
                    document_hava_morpheme_count+=1
            
            #tf = 문서내의 형태소빈도 / 문서내의 전체 형태소들의 빈도 ㄴ
            tf = morpheme.frequency / float(document_length)
            
            #idf = log(전체문서개수 / 형태소를 포함한 문서 개수)    #로그는 자연로그
            idf = math.log(len(crawled_knowledge_documents) / float(document_hava_morpheme_count))
            
            tfidf = tf * idf
            tfidf_dictionary[morpheme.morpheme] = tfidf
            
        sum_of_squared_tfidfs = 0
        for tfidf in tfidf_dictionary.values():
            sum_of_squared_tfidfs += tfidf**2
            
        normalization_value = math.sqrt(sum_of_squared_tfidfs)
        
        normalized_tfidf_dictionary = {}
        for morpheme, tfidf in tfidf_dictionary.items():
            normalized_tfidf = tfidf / normalization_value
            normalized_tfidf_dictionary[morpheme] = normalized_tfidf
        
        return  normalized_tfidf_dictionary
        
    def _filter_target_knowledge_document(self, knowledge, crawled_knowledge_documents):
        filtered_document = []
        
        for crawled_knowledge_document in crawled_knowledge_documents:
            if crawled_knowledge_document.knowledge_id == knowledge.id:
                crawled_knowledge_document.content = crawled_knowledge_document.content.encode('utf-8')
                filtered_document.append(crawled_knowledge_document)
            
        return filtered_document
        

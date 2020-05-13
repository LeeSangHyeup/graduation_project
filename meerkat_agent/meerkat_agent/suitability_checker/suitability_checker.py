#-*- coding: utf-8 -*-
'''
Created on 2014. 5. 12.

@author: lsh
'''

#meerkat modules
from temporary_data_management.keyword_management import KeywordManager
        

class SuitabilityChecker:
    '''
    1. checkKeywordCorrelation 키워드와 문서의 연관성 검사
    2. checkArticleSuitability 대상 문서의 국사분야와의 연관성 검사
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def check_keyword_correlation(self, search_keyword, morpheme_list):
        #정밀도(키워드가 형태소 순위에서 몇 %이내에 랭크되어야 연관성이 있는것으로 판단할지를 결정)
        precision=1*0.01
        
        hit_range = int(precision*(len(morpheme_list)))
        if hit_range==0:
            hit_range=1
        
        hit_range_morpheme_list = morpheme_list[0:hit_range]
        
        for morpheme in hit_range_morpheme_list:
            if search_keyword in morpheme.morpheme:
                return True
        
        return False;

    def check_pearson_correlation(self, x, y):
        n = len(x)
        vals = range(n)

        #합한다.
        sumx = sum([float(x[i]) for i in vals])
        sumy = sum([float(y[i]) for i in vals])
        #제곱을 합한다.
        sumx_sq = sum([x[i]**2.0 for i in vals])
        sumy_sq = sum([y[i]**2.0 for i in vals])
    
        #곱을 합한다.
        p_sum = sum([x[i]*y[i] for i in vals])
    
        #피어슨 점수를 계산한다.
        num = p_sum - (sumx * sumy / n)
        den = (sumx_sq - pow(sumx, 2) / n) * (sumy_sq - pow(sumy, 2)) ** 0.5
        
        if den == 0:
            return 0
        
        r = num / den
        
        return r

    def check_article_suitability(self, morpheme_list):
        #분석된 문서의 형태소 개수
        morpheme_quantity = len(morpheme_list)
        #적합성 검사의 기준점수
        pass_score = 3*morpheme_quantity
        
        if pass_score==0:
            return False
        
        #형태소의 가중치값에 곱해지는 값
        weight_value_benefit = 2
        #현재 적합성 평가를 하고있는 문서의 적합성 점수
        current_document_score = 0
        
        for morpheme in morpheme_list:
            keyword_manager = KeywordManager()
            row = keyword_manager.inquiry_morpheme(morpheme.morpheme)
            if row is None:
                continue
            
            weight_value = int(row)
            
            current_document_score += (weight_value * weight_value_benefit)

        if current_document_score >= pass_score:
            return True
    
        return False

        
        
        
        
        
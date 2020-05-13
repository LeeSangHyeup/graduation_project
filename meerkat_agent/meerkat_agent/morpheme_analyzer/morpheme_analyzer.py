#-*- coding: utf-8 -*-
'''
Created on 2014. 7. 5.

@author: lsh
'''

import os
import commands
import StringIO
import multiprocessing

#meerkat modules
from global_objects import CONFIG

class Morpheme:
    '''
    klt분석기의 결과를 이용하여 생성되는 형태소
    '''
    
    def __init__(self, morpheme, rank, frequency):
        self.morpheme = morpheme
        self.rank = rank
        self.frequency = frequency
        

class MorphemeAnalyzer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def analyze_morpheme(self, article):
        '''
        KLT-2010 형태소 분석기를 이용한 형태소 분석.
        !!주의!! 입력된 문서의 길이가 메우 길 경우에 형태소 분석이 되지않는 오류발생함.(리턴값 0 반환)
        '''
        txt_file_name = multiprocessing.current_process().name
        #추출된 본문을 KLT형태소분석기에 인자로 넘기기 위해 txt파일로 생성.
        temporary_article_txt_file = open(CONFIG.KLT_ANALYZER_PATH+'meerkatTemporaryFile/'+txt_file_name+'.txt','w')
        temporary_article_txt_file.write(str(article))
        temporary_article_txt_file.close()
        
        tmp_analyze_result_txt_file = CONFIG.KLT_ANALYZER_PATH+'meerkatTemporaryFile/'+txt_file_name+'.txt'
        
        assert os.path.isfile(tmp_analyze_result_txt_file), '형태소 분석기의 입력파일이 존재하지 않습니다'
        
        #klt형태소분석기를 작동시키는 리눅스 명령어
        analyzer_call_command = 'cd '+CONFIG.KLT_ANALYZER_PATH+'&& ./indexT ./meerkatTemporaryFile/'+txt_file_name+'.txt'
        analyze_result = commands.getoutput(analyzer_call_command)
        assert analyze_result is not None, '형태소 분석결과가 없습니다.'
        
        if os.path.isfile(tmp_analyze_result_txt_file):
            os.remove(tmp_analyze_result_txt_file)
        
        line_count=0
        result_line_list=[]
        
        #klt분석기의 출력결과에서 헤더영역의 라인수 변경하지 말것!
        klt_result_header_range=4
        
        for result_line in StringIO.StringIO(analyze_result):
            line_count+=1
            #형태소분석결과 중 헤더영역 생략 
            if line_count < klt_result_header_range:
                continue
            
            result_line_list.append(result_line) 
            
        #형태소분석결과 중 footer영역 삭제 후 반환
        result_line_list = result_line_list[:-1]
        
        return self._create_morpheme_list(result_line_list)
        
    def _create_morpheme_list(self, analyze_result):
        '''
        KLT 형태소 분석기의 분석결과를 입력받아 형태소객체의 리스트로 만들어 반환.
        '''
        morpheme_list = []
        for result_line in analyze_result:
            result_line=result_line.strip()
            result_tokens=result_line.split()
            
            if len(result_tokens) < 4:
                continue
            
            morpheme = result_tokens[3].strip()
            rank = int(result_tokens[0].strip()[:-1])
            frequency = int(result_tokens[1].strip())
            
            morpheme_list.append(Morpheme(morpheme, rank, frequency))
        
        return morpheme_list

    def calculate_rank(self, keyword, morpheme_list):
        for morpheme in morpheme_list:
            if not keyword == morpheme.morpheme:
                continue
            
            #형태소리스트에서 대상 키워드와 동일한 형태소의 순위를 반환
            return morpheme.rank
        
        return False
                
    def extract_korean_alphabet(self, string):
        #문자열로 부터 한글을 추출
        korean_alphabet = filter(lambda c: c > '\x7f', string)
        
        korean_alphabet = korean_alphabet.strip()
        #추출된 문자열에 한글이 없으면 False 반환
        if korean_alphabet=='':
            return None
        
        return korean_alphabet
        
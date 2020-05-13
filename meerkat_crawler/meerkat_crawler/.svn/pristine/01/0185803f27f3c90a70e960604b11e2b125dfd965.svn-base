#-*- coding: utf-8 -*-
import os
import commands
import StringIO
import multiprocessing

class Morpheme:
    '''
    klt분석기의 결과를 이용하여 생성되는 형태소
    '''
    
    def __init__(self, morpheme, rank, frequency):
        self.morpheme = morpheme
        self.rank = rank
        self.frequency = frequency
        
def check_pure_korean_alphabet(string):
        #문자열로 부터 한글을 추출
        korean_alphabets = filter(lambda c: c > '\x7f', string)
        
        if len(string) != len(korean_alphabets):
            return False
        
        return True

class MorphemeAnalyzer:
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
        temporary_data_directory = 'temporary_data/'
        #추출된 본문을 KLT형태소분석기에 인자로 넘기기 위해 txt파일로 생성.
        temporary_article_txt_file = open(temporary_data_directory+txt_file_name+'.txt','w')
        temporary_article_txt_file.write(str(article))
        temporary_article_txt_file.close()
        
        tmp_analyze_result_txt_file = temporary_data_directory + txt_file_name+'.txt'
        
        assert os.path.isfile(tmp_analyze_result_txt_file), '형태소 분석기의 입력파일이 존재하지 않습니다'
        
        #klt형태소분석기를 작동시키는 리눅스 명령어
        analyzer_call_command = 'cd KLT2010-TestVersion/EXE && ./indexT ../../' + temporary_data_directory + txt_file_name+'.txt'
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
            
            #2글자 미만이면 해당 키워드 제외
            if morpheme.strip() in '백과':
                continue
            
            if morpheme.strip() in '위키':
                continue
            
            if morpheme.strip() in '사전':
                continue
            
            if len(morpheme.strip()) < 6:
                continue
            
            if check_pure_korean_alphabet(morpheme) == False:
                continue

            rank = int(result_tokens[0].strip()[:-1])
            frequency = int(result_tokens[1].strip())
            
            same_morpheme = filter(lambda x:x.morpheme==morpheme, morpheme_list)
            if len(same_morpheme)!=0:
                same_morpheme[0].frequency+=frequency
            else:
                morpheme_list.append(Morpheme(morpheme, rank, frequency))
        
        return morpheme_list

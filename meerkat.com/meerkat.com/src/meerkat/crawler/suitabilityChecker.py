#-*- coding: utf-8 -*-
'''
Created on 2014. 5. 12.

@author: lsh
'''

import os
import commands
import StringIO
import multiprocessing

from django.db import connection

from pathfinder.models import Morpheme
from meerkat.settings import KLT_ANALYZER_PATH

class SuitabilityChecker:
    '''
    1. checkKeywordCorrelation 키워드와 문서의 연관성 검사
    2. checkArticleSuitability 대상 문서의 국사분야와의 연관성 검사
    3. analyzeMorpheme 대상 문서의 현태소를 추출하여 리스트로 반환
    4. calculateMorphemeRank 대상 문서내에서 인자로 받은 형태소의 빈도 순위를 얻어냄 
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def checkKeywordCorrelation(self, searchKeyword, analyzeResult):
        #정밀도(키워드가 형태소 순위에서 몇 %이내에 랭크되어야 연관성이 있는것으로 판단할지를 결정)
        precision=1*0.01
        
        hitRange = int(precision*(len(analyzeResult)))
        if hitRange==0: hitRange=1
        
        resultLineList = analyzeResult[0:hitRange]
        
        for resultLine in resultLineList:
            if searchKeyword in resultLine:
                return True
        
        return False;

    def checkArticleSuitability(self, analyzeResult):
        #분석된 문서의 형태소 개수
        analyzeResultMorphemeCount = len(analyzeResult)
        #적합성 검사의 기준점수
        passScore = 3*analyzeResultMorphemeCount
        
        if passScore==0 : return False
        
        #형태소의 가중치값에 곱해지는 값
        weightValueBenefit = 2
        #현재 적합성 평가를 하고있는 문서의 적합성 점수
        currentDocumentScore = 0
        
        for resultLine in analyzeResult:
            resultLine=resultLine.strip()
            resultTokens=resultLine.split()
            
            if len(resultTokens) < 4 :continue
            morpheme = resultTokens[3]

            connection.close()
            try:analyzedMorpheme = Morpheme.objects.get(morpheme=morpheme)
            except:continue
            
            currentDocumentScore += (analyzedMorpheme.weightValue * weightValueBenefit)
        
        print 'passScore='+str(passScore)+', currentDocuScore='+str(currentDocumentScore)
        if currentDocumentScore >= passScore:return True
    
        return False
        
    def analyzeMorpheme(self, article):
        txtFileName = multiprocessing.current_process().name
        #추출된 본문을 KLT형태소분석기에 인자로 넘기기 위해 txt파일로 생성.
        temporaryArticleTxtFile = open(KLT_ANALYZER_PATH+'meerkatTemporaryFile/'+txtFileName+'.txt','w')
        temporaryArticleTxtFile.write(str(article))
        temporaryArticleTxtFile.close()
        
        #klt형태소분석기를 작동시키는 리눅스 명령어
        tmpAnalyzeResultTxtFile = KLT_ANALYZER_PATH+'meerkatTemporaryFile/'+txtFileName+'.txt'
        
        assert os.path.isfile(tmpAnalyzeResultTxtFile), '형태소 분석기의 입력파일이 존재하지 않습니다'
        if not os.path.isfile(tmpAnalyzeResultTxtFile):return False

        analyzerCallCommand = 'cd '+KLT_ANALYZER_PATH+'&& ./indexT ./meerkatTemporaryFile/'+txtFileName+'.txt'
        analyzeResult = commands.getoutput(analyzerCallCommand)
        
        if os.path.isfile(tmpAnalyzeResultTxtFile):
            os.remove(tmpAnalyzeResultTxtFile)
        
        lineCount=0
        resultLineList=[]
        
        #klt분석기의 출력결과에서 헤더영역의 라인수 변경하지 말것!
        kltResultHeaderRange=4
        
        for resultLine in StringIO.StringIO(analyzeResult):
            lineCount+=1
            #형태소분석결과 중 헤더영역 생략 
            if lineCount < kltResultHeaderRange:continue
            resultLineList.append(resultLine)
            
        #형태소분석결과 중 footer영역 삭제 후 반환
        return resultLineList[:-1]
    
    def calculateMorphemeRank(self, targetMorpheme, resultLineList):
        for resultLine in resultLineList:
            if not targetMorpheme in resultLine:continue
            #찾은 형태소검색결과줄에서 순위만 추출
            resultLine = resultLine.strip()
            resultLine = resultLine.split()
            rankToken = resultLine[0]
            rankToken = rankToken[:-1]
            rank = int(rankToken)
            return rank
        
        return False
                
        
        
        
        
        
        
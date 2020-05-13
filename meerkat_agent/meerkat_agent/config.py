#-*- coding: utf-8 -*-
'''
Created on 2014. 6. 23.

@author: lsh
'''

'''
config file for agent
'''
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Config():
    _CONFIG_FILE_NAME = 'config.txt'
    ROOT_PATH = os.path.dirname(__file__)
    
    def __init__(self):
        config_file=None
        
        if os.path.isfile(self._CONFIG_FILE_NAME):
            config_file=open(self._CONFIG_FILE_NAME, 'r')
        else:
            config_file=self._set_default_config(self._CONFIG_FILE_NAME)
            config_file=open(self._CONFIG_FILE_NAME, 'r')
        
        self._apply_config(config_file)
        config_file.close()
    
    def _set_default_config(self, config_file_name):
        config_file=open(config_file_name, 'w')
        
        config_file.write('''\
###config file for meerkat agent


#수집할 문서의 분야
CATEGORY='국사'

#웹 검색 시에 가동할 프로세스 개수를 결정하는 값(프로세스 개수 = cpu코어개수 * CRAWLER_PROCESS_WEIGHTVALUE)
CRAWLER_PROCESS_WEIGHTVALUE=4

#url서버 접속정보
URL_SERVER_HOST='localhost'
URL_SERVER_PORT='2222'

#db서버 접속정보
DBMS_NAME='postgresql'
DB_HOST='192.168.0.4'
DB_PORT='5432'
DB_NAME='meerkat'
DB_USER='postgres'
DB_PASSWORD='00000NUL(null)'

#한국어 형태소분석기의 경로
KLT_ANALYZER_PATH='/external_modules/KLT2010-TestVersion/EXE/'
        ''')
        
        config_file.flush()
    
    def _apply_config(self, config_file):
        line_count=0
        for each_line in config_file.xreadlines():
            line_count+=1
            
            if each_line.startswith('#'):
                continue
            if each_line.strip()=='':
                continue
            if len(each_line.split('='))!=2:
                self._exit_with_print_config_file_error_message(each_line, line_count)
            
            each_line=each_line.strip()
            argument, value = each_line.split('=')
            value=value.replace("'", '')
            
            if argument=='CATEGORY':
                self.CATEGORY=value
            elif argument=='CRAWLER_PROCESS_WEIGHTVALUE':
                self.CRAWLER_PROCESS_WEIGHTVALUE=int(value)
            elif argument=='URL_SERVER_HOST':
                self.URL_SERVER_HOST=value
            elif argument=='URL_SERVER_PORT':
                self.URL_SERVER_PORT=value
            elif argument=='DBMS_NAME':
                self.DBMS_NAME=value
            elif argument=='DB_HOST':
                self.DB_HOST=value
            elif argument=='DB_PORT':
                self.DB_PORT=value
            elif argument=='DB_NAME':
                self.DB_NAME=value
            elif argument=='DB_USER':
                self.DB_USER=value
            elif argument=='DB_PASSWORD':
                self.DB_PASSWORD=value
            elif argument=='KLT_ANALYZER_PATH':
                self.KLT_ANALYZER_PATH=self.ROOT_PATH + value
            else:
                self._exit_with_print_config_file_error_message(each_line, line_count)
            
    def _exit_with_print_config_file_error_message(self, error_line, line_count):
        line_count = str(line_count)
        print "CONFIG FILE ERROR: '" + self._CONFIG_FILE_NAME + \
            "' contain error at line " + line_count + "\nline(" + line_count + "): " + error_line
        sys.exit()


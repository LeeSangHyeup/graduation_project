#-*- coding: utf-8 -*-
'''
Created on 2014. 6. 23.

@author: lsh
'''

'''
config file for pathfinder
'''


import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Config:
    _CONFIG_FILE_NAME = 'config.txt'
    ROOT_PATH = os.path.dirname(__file__)
    
    def __new__(cls):
        #apply singleton
        if not hasattr(cls, 'instance'):
            cls.instance=super(Config, cls).__name__(cls)
        return cls.instance
    
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

#지식지도 생성시 사용할 프로세스의 개수
PATHFINDER_PROCESS_QUANTITY=4

#keyword서버의 포트번호
KEYWORD_SERVER_PORT=2223

#keyword서버의 IP주소
KEYWORD_SERVER_IP='192.168.0.4'

#document서버의 포트번호
DOCUMENT_SERVER_PORT=2224

#document서버의 IP주소
DOCUMENT_SERVER_IP='192.168.0.4'
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
            elif argument=='PATHFINDER_PROCESS_QUANTITY':
                self.PATHFINDER_PROCESS_QUANTITY=int(value)
            elif argument=='KEYWORD_SERVER_PORT':
                self.KEYWORD_SERVER_PORT=int(value)
            elif argument=='KEYWORD_SERVER_IP':
                self.KEYWORD_SERVER_IP=value
            elif argument=='DOCUMENT_SERVER_PORT':
                self.DOCUMENT_SERVER_PORT=int(value)
            elif argument=='DOCUMENT_SERVER_IP':
                self.DOCUMENT_SERVER_IP=value
            else:
                self._exit_with_print_config_file_error_message(each_line, line_count)
            
    def _exit_with_print_config_file_error_message(self, error_line, line_count):
        line_count = str(line_count)
        print "CONFIG FILE ERROR: '" + self._CONFIG_FILE_NAME + \
            "' contain error at line " + line_count + "\nline(" + line_count + "): " + error_line
        sys.exit()


CONFIG = Config()
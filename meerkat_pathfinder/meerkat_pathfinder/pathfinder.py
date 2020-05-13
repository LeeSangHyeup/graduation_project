'''
Created on 2014. 8. 29.

@author: lsh
'''


import time
import xmlrpclib

#meerkat modules
from config import CONFIG 


class Pathfinder:

    def __init__(self):
        self._keyword_server_proxy = xmlrpclib.ServerProxy(
           'http://'+CONFIG.KEYWORD_SERVER_IP+':'+str(CONFIG.KEYWORD_SERVER_PORT))
        self._document_server_proxy = xmlrpclib.ServerProxy(
           'http://'+CONFIG.DOCUMENT_SERVER_IP+':'+str(CONFIG.DOCUMENT_SERVER_PORT))
        
    def pathfind(self):
        while True:
            target_keyword = self._keyword_server_proxy.request_candidate_keyword()
            
            if target_keyword == None:
                time.sleep(1)
                continue
               
            offset = 0
            
    def pathfind_process(self):
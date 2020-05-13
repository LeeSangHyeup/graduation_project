'''
Created on 2014. 8. 27.

@author: lsh
'''

import logging

#meerkat modules
from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler()
    
    print 'crawler activated'
    
    logging.info("Server Start..")
    
    try:
        crawler.collect_document()
    except:
        logging.exception('')
'''
Created on 2014. 7. 27.

@author: lsh
'''

import pickle

#meerkat_modules
from models.xmlrpc import CrawledKnowledgeDocument


def transmit_crawled_knowledge  _documents(topic, documents):
    crawled_knowledge_documents = []
    
    for document in documents:
        crawled_knowledge_document = CrawledKnowledgeDocument(
            document['knowledge_name'],
            document['url'],
            document['title'],
            document['content'],
            document['topics'],
            document['corrected_date'],
                )
        
        crawled_knowledge_documents.append(crawled_knowledge_document)
    
    
    return True



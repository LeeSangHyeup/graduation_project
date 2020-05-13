'''
Created on 2014. 8. 27.

@author: lsh
'''


class CrawledKnowledgeDocument:
    def __init__(self, knowledge_name, url, title, content, topics, corrected_date):
        self.knowledge_name = knowledge_name
        self.url = url
        self.title = title
        self.content = content
        self.topics = topics
        self.corrected_date = corrected_date
    
    
class WithoutKnowledgeDocument:
    def __init__(self, url, title, content, corrected_date, topics):
        self.url = url
        self.title = title
        self.content = content
        self.topics = topics
        self.corrected_date = corrected_date
        
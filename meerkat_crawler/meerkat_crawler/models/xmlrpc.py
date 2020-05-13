'''
Created on 2014. 8. 28.

@author: lsh
'''

class Document:
    def __init__(self, knowledge_name, url, title, content):
        self.knowledge_name = knowledge_name
        self.url = url
        self.title = title
        self.content = content
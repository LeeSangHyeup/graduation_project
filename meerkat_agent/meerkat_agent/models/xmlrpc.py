'''
Created on 2014. 7. 26.

@author: lsh
'''

class CandidateUrl(object):
    def __init__(self, url, seed_url):
        self.url = url
        self.seed_url = seed_url
        
class Seed(object):
    def __init__(self, url, hit_url):
        self.url = url
        self.hit_url = hit_url
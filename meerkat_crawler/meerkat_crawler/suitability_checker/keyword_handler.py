#-*- coding: utf-8 -*-
class KeywordHandler:
    def __init__(self):
        pass

    def inquiry_history_keyword(self, keyword):
        assert keyword != None, 'keyword is invalid'
        assert len(keyword) > 0, 'keyword is invalid'

        with open('suitability_checker/history_keyword_list.txt', 'r') as history_keyword_list_file:
            for each_line in history_keyword_list_file.xreadlines():
                each_line = each_line.split('/')
                inquiry_keyword = each_line[0]

                if inquiry_keyword == keyword:
                    frequency = int(each_line[1])
                    document_frequency = int(each_line[2].strip())
            
                    return inquiry_keyword, frequency, document_frequency 

        return None

    def inquiry_not_history_keyword(self, keyword):
        assert keyword != None, 'keyword is invalid'
        assert len(keyword) > 0, 'keyword is invalid'

        with open('suitability_checker/not_history_keyword_list.txt', 'r') as not_history_keyword_list_file:
            for each_line in not_history_keyword_list_file.xreadlines():
                each_line = each_line.split('/')
                inquiry_keyword = each_line[0]

                if inquiry_keyword == keyword:
                    frequency = int(each_line[1])
                    document_frequency = int(each_line[2].strip())
            
                    return keyword, frequency, document_frequency 

        return None

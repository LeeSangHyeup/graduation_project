from keyword_handler import KeywordHandler
from morpheme_analyzer.morpheme_analyzer import MorphemeAnalyzer


class KoreanHistoryClassifier:
    def __init__(self):
        self._history_probability = 0.5
        self._not_history_probability = 0.5
        #4000(history_document) + 4000(not_history_document) = 8000 
        self._document_quantity = 4000
        self._keyword_handler = KeywordHandler()
        self._morpheme_analyzer = MorphemeAnalyzer()

    def binary_classify(self, article):
        assert article != None, 'article is invalid'
        assert len(article) > 0, 'article is invalid'

        total_positive_score = 1
        total_negative_score = 1

        morpheme_list = MorphemeAnalyzer().analyze_morpheme(article)

        for morpheme in morpheme_list:
            history_inquiry_result = self._keyword_handler.inquiry_history_keyword(morpheme.morpheme)
            not_history_inquiry_result = self._keyword_handler.inquiry_not_history_keyword(morpheme.morpheme)
            
            positive_score = self._compute_positive_score(history_inquiry_result, not_history_inquiry_result)
            negative_score = self._compute_negative_score(history_inquiry_result, not_history_inquiry_result)
            
            total_positive_score *= (positive_score**morpheme.frequency)
            total_negative_score *= (negative_score**morpheme.frequency)

        if total_positive_score < total_negative_score:
            #this document classified in history category
            return True
        else:
            #this document classified in not history category
            return False

    def _compute_positive_score(self, history_inquiry_result, not_history_inquiry_result):
        positive_score = None
            
        if history_inquiry_result == None:
            positive_score = (self._history_probability + 1) / 1
        else:
            history_document_frequency = float(history_inquiry_result[2])
            not_history_document_frequency = 0
            if not_history_inquiry_result != None:
                not_history_document_frequency = not_history_inquiry_result[2]
            
            history_appearance_probability = history_document_frequency / self._document_quantity
            total_appearance_probability = (history_document_frequency + not_history_document_frequency) / (self._document_quantity * 2)

            positive_score = (history_appearance_probability * self._history_probability + 1) / (total_appearance_probability + 1)

        return positive_score
            
    def _compute_negative_score(self, history_inquiry_result, not_history_inquiry_result):
        negative_score = None
            
        if not_history_inquiry_result == None:
            negative_score = (self._not_history_probability + 1) / 1
        else:
            history_document_frequency = 0
            if history_inquiry_result != None:
                history_document_frequency = history_inquiry_result[2]
            not_history_document_frequency = float(not_history_inquiry_result[2])
            
            not_history_appearance_probability = not_history_document_frequency / self._document_quantity
            total_appearance_probability = (history_document_frequency + not_history_document_frequency) / (self._document_quantity * 2)

            negative_score = (not_history_appearance_probability * self._history_probability + 1) / (total_appearance_probability + 1)

        return negative_score

# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
from django.db import connection
from knowledge.models import Knowledge
from meerkat.settings import TEMPLATE_DIRS
from crawler.models import CrawledKnowledgeDocument

def searchPage(request):
    if request.GET.has_key('searchKeyword') == False:
        return HttpResponseRedirect('/')
    elif len(request.GET['searchKeyword']) == 0:
        return HttpResponseRedirect('/')

    searchKeyword = request.GET['searchKeyword'].encode('utf8')

    try:
        knowledgies = Knowledge.objects.filter(knowledge_name__contains = searchKeyword)
    except:
        return HttpResponseRedirect('/')

    crawledKnowledgeDocuments = []
    
    for knowledge in knowledgies:
        documents = CrawledKnowledgeDocument.objects.filter(knowledge=knowledge)
        
        for document in documents:
            contentLength = len(document.content)
            if contentLength > 200:
                document.content = document.content[:200]+'...'
            crawledKnowledgeDocuments.append(document)
         
        
    context=Context({
        'user':request.user,
        'base':TEMPLATE_DIRS[0]+'/common/base.html',
        'crawledKnowledgeDocuments':crawledKnowledgeDocuments,
             })
    connection.close()
    return render_to_response("knowledge/search_page.html", context)



from django.contrib import admin
from models import CrawledKnowledgeDocument

class CrawledKnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'knowledge', 'title', 'url')
 
admin.site.register(CrawledKnowledgeDocument, CrawledKnowledgeDocumentAdmin)

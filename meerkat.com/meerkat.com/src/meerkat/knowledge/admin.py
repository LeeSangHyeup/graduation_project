from django.contrib import admin
from knowledge.models import Category
from knowledge.models import Knowledge


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)

class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'knowledge_name',)
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Knowledge, KnowledgeAdmin)
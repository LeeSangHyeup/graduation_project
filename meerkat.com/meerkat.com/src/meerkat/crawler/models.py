from django.db import models
from knowledge.models import Knowledge

class CrawledKnowledgeDocument(models.Model):
    knowledge = models.ForeignKey(Knowledge, null=False)
    url = models.TextField(null=False, unique=True)
    title = models.CharField(max_length=80, null=False)
    content = models.TextField(null=False)
    corrected_date = models.DateTimeField(auto_now_add=True, auto_now=True)
    def __unicode__(self):
        return self.title

from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=40, null=False, unique=True)
    def __unicode__(self):
        return self.category_name
    
class Knowledge(models.Model):
    category = models.ForeignKey(Category)
    associated_knowledge = models.ManyToManyField('self', null=True)
    knowledge_name = models.CharField(max_length=50, null=False, unique=True)
    def __unicode__(self):
        return self.knowledge_name

from django.db import models

class Category(models.Model):
    name = models.CharField( max_length=200,null=True)
    description = models.CharField(max_length=200 ,null=True)
    
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='category',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
                            null=True)

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.

class Ingredient(models.Model):
    amount = models.IntegerField()
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Cuisine(models.Model):
    name = models.CharField(max_length=100)
    taste = models.CharField(max_length=100)
    review = models.TextField(max_length=500)
    type = models.CharField(max_length=100)
    prep_time = models.IntegerField()
    def __str__(self):
        return self.name


from django.db import models



class Store(models.Model):
   

    name = models.CharField(max_length=20,blank=False, primary_key=True)
    description = models.CharField(max_length=15, blank=False, default="")
    logo = models.CharField(max_length=30,blank=False, default="")
    tags = models.CharField(max_length=30,blank=False, default="")
    likes = models.IntegerField(default=1)
    

from django.db import models

# Create your models here.
class Url(models.Model):
    originalurl = models.CharField(max_length=300)
    description = models.TextField(default=None, blank=True, null=True)

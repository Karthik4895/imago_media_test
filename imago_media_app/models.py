from django.db import models


class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

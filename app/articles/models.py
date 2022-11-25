"""Article Model"""

from django.db import models


class Article(models.Model):
    """This Is Articles Model"""
    title = models.CharField(max_length=255)
    short_information = models.TextField()
    is_published = models.BooleanField(default=False)
    total_approved = models.IntegerField(default=0)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

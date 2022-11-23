"""Article Connection With Approval Of People"""

from django.db import models
from ..articles import Article
# Create your models here.


class ArticleApproval(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

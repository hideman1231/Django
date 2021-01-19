from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
	title = models.CharField(max_length=50)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
	article_created = models.DateTimeField(auto_now_add=True, blank=True)
	article_updated = models.DateTimeField(auto_now=True)
	article_like = models.ManyToManyField(User, null=True, blank=True)

	def __str__(self):
		return f'{self.title} | {self.author} | like - {self.article_like.count()} | {self.article_created}'


class Comment(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
	content = models.TextField()
	comment_created = models.DateTimeField(auto_now_add=True, blank=True)
	comment_updated = models.DateTimeField(auto_now=True)
	comment_like = models.ManyToManyField(User, related_name='comment_likes', null=True, blank=True)
	comment = models.ForeignKey('myapp.Comment', blank=True, null=True, on_delete=models.CASCADE, related_name='comments')

	def __str__(self):
		if self.comment:
			return f'comment for comment {self.content[:10]} | {self.author} | like - {self.comment_like.count()} | {self.comment_created}'
		else:
			return f'comment for article {self.article.title} | {self.author} | like - {self.comment_like.count()} | {self.comment_created}'


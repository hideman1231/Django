from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Article(models.Model):
	title = models.CharField('article name', max_length=50)
	content = models.TextField('article content')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_author')
	article_created = models.DateTimeField('article creation', default=timezone.now)
	article_updated = models.DateTimeField('article update', auto_now=True)

	def __str__(self):
		return f'{self.title} | {self.author} | {self.article_created} | {ArticleLike.objects.filter(like__title=self.title).count()} likes | {ArticleDislike.objects.filter(dislike__title=self.title).count()} dislikes'

class Comment(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
	content = models.TextField('comment content')
	comment_created = models.DateTimeField('comment creation', default=timezone.now)
	comment_updated = models.DateTimeField('comment update', auto_now=True)
	comment = models.ForeignKey('myapp.Comment', blank=True, null=True, on_delete=models.CASCADE, related_name='comments')

	def __str__(self):
		if self.comment:
			return f'Comment for comment: {self.content[:10]} | {self.author} | {self.comment_created} | {CommentLike.objects.filter(like__comment=self.comment).count()} likes | {CommentDislike.objects.filter(dislike__comment=self.comment).count()} dislikes'
		else:
			return f'Comment for article: {self.article.title} | {self.author} | {self.comment_created} | {CommentLike.objects.filter(like__article=self.article).count()} likes | {CommentDislike.objects.filter(dislike__article=self.article).count()} dislikes'


class ArticleLike(models.Model):
	like = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_like')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_author_like')


class ArticleDislike(models.Model):
	dislike = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_dislike')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_author_dislike')


class CommentLike(models.Model):
	like = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author_like')


class CommentDislike(models.Model):
	dislike = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_dislike')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author_dislike')


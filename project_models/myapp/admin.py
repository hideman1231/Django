from django.contrib import admin

from myapp.models import Article, Comment, ArticleLike, ArticleDislike, CommentLike, CommentDislike

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(ArticleLike)
admin.site.register(ArticleDislike)
admin.site.register(CommentLike)
admin.site.register(CommentDislike)

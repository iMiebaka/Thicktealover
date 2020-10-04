from django.contrib.sitemaps import Sitemap
from blog.models import Post
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefre = 'daily'
    priority = 1.0

    def items(self):
        return['blog_contact',]
    
    def reverse(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    changefre = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.filter(published_flag=True, status='Ready')
    
    def lastmod(self, obj):
        return obj.last_modified
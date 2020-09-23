from django.contrib import admin
from blog.models import Post, Category,Comment

class PostAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class TagsAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Post) 
admin.site.register(Category)
admin.site.register(Comment)
# admin.site.register(Tags)
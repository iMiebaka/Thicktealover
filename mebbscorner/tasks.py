from background_task import background
from django.contrib.auth.models import User
from blog.models import Post, Comment, Profile, Post_views


@background(schedule=6)
def notify_user():
    pass
    # print('helloee')
    post_qs = Post.objects.filter(published_flag=True, status='Ready')
    # Updating number of Comment
    for p in post_qs:
        comment_ammount = Comment.objects.filter(post=p.id).count()
        post_view = Post.objects.get(id=pm.id)
        post_view.number_of_comments = comment_ammount
        post_view.save()
    
    #Updating number of post in profile
    for p in post_qs:
        view_post = Post.objects.filter(published_flag=True, status='Ready', author=p.author_id).count()
        edit_views = Profile.objects.get(user_id=p.author_id)
        edit_views.number_of_post = view_post
        edit_views.save()
    
    #Updating number of views in profile
    for p in post_qs:
        view_post = Post_views.objects.filter(post=p.id).count()
        edit_views = Profile.objects.get(user_id=p.author_id)
        edit_views.number_of_views = view_post
        edit_views.save()

def notify_user2():
    pass
    print('hello')
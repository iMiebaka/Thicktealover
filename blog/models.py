from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# from taggit.managers import TaggableManager
User = settings.AUTH_USER_MODEL
from .select_options import COUNTRY, REQUEST_DEFAULT, published_choice_admin, published_choice_staff



class Tags(models.Model):
    name = models.CharField(max_length=20, unique=True)
    added_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    added_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
  
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('category_archive', kwargs={'slug': self.slug})


class Post(models.Model):
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, related_name='publisher') 
    title = models.CharField(max_length=30, verbose_name="Post title")
    slug = models.SlugField(unique=True, max_length=100, null=True)
    body = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(default='big_img_1.jpg', upload_to='images/') 
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    published_flag = models.BooleanField(null=True, default=False)
    status = models.CharField(max_length=7, null=True)
    number_of_comments = models.IntegerField(null=True)
    favorite = models.BooleanField(null=True)
    read_duration = models.IntegerField(null=True, default=3)
    number_of_views = models.IntegerField(null=True, default=0)
    new_tag = models.ManyToManyField('Tags', related_name='tag')
    categories = models.ManyToManyField('Category', related_name='posts')
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='approval_officer' )

    def __str__(self):
        return self.title 

    # def get_absolute_url(self):
    #     return reverse('blog_detail', kwargs={'slug': self.slug})
    
class Post_views(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postview')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
class Post_liked(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postliked')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40, null=True)
    created = models.DateTimeField(auto_now_add=True)

class Follower_list(models.Model):
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_user')
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user')

class Comment(models.Model):
    name = models.CharField(max_length=80)#, default="Anonymous")
    url = models.URLField(max_length=80, null=True)#, default="Anonymous")
    email = models.EmailField(max_length=200)
    body = models.CharField(max_length=250, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author_voice = models.BooleanField(null=True, default=False)
    co_author_voice = models.BooleanField(null=True, default=False)
    active_writer = models.BooleanField(null=True, default=False)
    active_writer_inst = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    # class Meta:
    #     # sort comments in chronological order by default
    #     ordering = ("-created_on")

    def __str__(self):
        return 'Comment by {}'.format(self.name)

class Newsletter_subcribers(models.Model):
    email = models.EmailField(max_length=200,unique=True)
    verified = models.BooleanField(null=True, default=False)
    created_on = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    number_of_post = models.IntegerField(null=True)
    number_of_views = models.IntegerField(null=True, default=0)
    profile_complete = models.BooleanField(null=True, default=False)
    birth_date = models.DateField(null=True , blank=True)
    bio = models.TextField(max_length=200 , null=True, blank=True)
    sex = models.CharField(max_length=6 , null=True, blank=True)
    location = models.CharField(max_length=30 , choices=COUNTRY, null=True, blank=True)
    cover_image = models.ImageField(default='default_image.jpg', null=True, upload_to='profile/images/') 
    linkedin = models.URLField(max_length=80, null=True)
    twitter = models.URLField(max_length=80, null=True)
    github = models.URLField(max_length=80, null=True)
    whatsapp = models.URLField(null=True)
    visibility = models.BooleanField(null=True, default=False)

    def __str__(self):
        return str(self.user)


class Collaburating_author(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    key = models.CharField(max_length=30, unique=True)
    created_on = models.DateField(auto_now_add=True)
    approved_on = models.DateField(null=True)
    status = models.BooleanField(default=False, null=True)
    requested_status = models.BooleanField(default=True, null=True)
    request_accepted = models.BooleanField(default=False, null=True)
    author_in_request = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='collaburatee')
    requested_author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='collaburation_requested_by')
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='collaburation_approved_by')
    
    def __str__(self):
        return str(self.key)

class Post_history(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    created_on = models.DateField(null=True, auto_now_add=True)
    description = models.CharField(null=True, max_length=30)
    state = models.CharField(null=True, max_length=30)

class Contact_us(models.Model):
    first_name = models.CharField(max_length=15 , null=True)
    last_name = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=20, null=True)
    phone_number = models.IntegerField(null=True)
    messages = models.CharField(max_length=70 , null=True)

class Author_request(models.Model):
    username = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, related_name='requst_publisher') 
    title = models.CharField(unique=True, max_length=30 , null=True)
    encodededpk = models.CharField(unique=True, max_length=5, null=True)
    weight = models.CharField(max_length=10, default='Heavy')
    message = models.CharField(unique=True, max_length=100 , null=True)
    markas_read = models.BooleanField(default=False, null=True)
    created_on = models.DateField(auto_now_add=True, null=True)
    modified_on = models.DateField(auto_now=True, null=True)
    message_to = models.ForeignKey(User, null=True, on_delete = models.SET_NULL) 
    approved_by = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, related_name='requst_approval') 

class Author_request_category(models.Model):
    username = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, related_name='requst_cat_publisher') 
    options = models.CharField(max_length=20 , null=True, default='Request Category')
    category = models.CharField(unique=True, max_length=30 , null=True)
    status = models.CharField(max_length=30 , null=True)
    created_on = models.DateField(auto_now_add=True, null=True)
    approved = models.BooleanField(default=False, null=True)
    modified_on = models.DateField(null=True)
    approved_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL, related_name='requst_cat_approval') 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

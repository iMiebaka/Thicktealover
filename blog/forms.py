from django import forms
from django.forms import ModelForm
from .models import Comment, Post, Category, Tags, Author_request, Author_request_category, Contact_us, Collaburating_author, Profile
from .select_options import COUNTRY, REQUEST_DEFAULT, published_choice_admin, published_choice_staff
from ckeditor.fields import RichTextField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User

# from ckeditor_uploader.widgets import CKEditorWidget, CKEditorUploadingWidget


class CommentForm(forms.ModelForm):
    name = forms.CharField(required=True, widget= forms.TextInput(attrs={"class": "form-control", "placeholder": "Name" }))
    email = forms.CharField(required=True, widget= forms.TextInput(attrs={"class": "form-control", "placeholder": "Email" }))
    url = forms.URLField(required=False, widget= forms.TextInput(attrs={"class": "form-control", "placeholder": "URL"}))
    body = forms.CharField(required=True, widget= forms.Textarea(attrs={"class": "form-control", "placeholder": "Comment" }))
    class Meta:
        model = Comment
        fields = ('name', 'email', 'url', 'body')
        widgets = {
    }
    
class CommentForm_author(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={"class": "form-control", "required": "true", "placeholder": "Comment" })
    }

class ArticlesForm(forms.ModelForm):  
    class Meta:  
        model = Category 
        fields = ['name']

class TagForm(forms.ModelForm):  
    class Meta:  
        model = Tags 
        fields = ['name']

class BlogForm(forms.ModelForm):  
    class Meta:
        model = Post
        fields = ['title', 'body', 'published_flag']


class PostForms(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control col-md-6", "placeholder": "Blog Title" }))
    body = forms.CharField(widget=CKEditorUploadingWidget(attrs={"class": "form-control"}))
    categories = forms.ModelMultipleChoiceField(queryset = Category.objects.all(), to_field_name="name", 
    widget=forms.SelectMultiple(attrs={"class": "form-control col-md-3"}))
    # published_flag = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    status  = forms.CharField(widget=forms.Select(choices=published_choice_admin, attrs={"class": "form-control form-control-lg col-md-3", 'data-role': "select-dropdown"}))
    favorite = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    read_duration = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "form-control col-md-3", "value": "3", "min": "1"}))
    cover_image = forms.ImageField(required=False, error_messages={'invalid':("Image files only")}, widget=forms.FileInput)
    remove_photo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    
    class Meta():
        model = Post
        fields = ('title', 'body', 'read_duration', 'status', 'published_flag', 'favorite', 'categories', 'cover_image')#, 'new_tag' ]


class PostForms2(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control col-md-6", "placeholder": "Blog Title" }))
    body = forms.CharField(widget=CKEditorUploadingWidget(attrs={"class": "form-control"}))
    categories = forms.ModelMultipleChoiceField(queryset = Category.objects.all(), to_field_name="name", 
    widget=forms.SelectMultiple(attrs={"class": "form-control col-md-3"}))
    # published_flag = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    status  = forms.CharField(widget=forms.Select(choices=published_choice_staff, attrs={"class": "form-control form-control-lg col-md-3", 'data-role': "select-dropdown"}))
    favorite = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    read_duration = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "form-control col-md-3", "value": "3", "min": "1"}))
    cover_image = forms.ImageField(required=False, error_messages={'invalid':("Image files only")}, widget=forms.FileInput)
    remove_photo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    

    class Meta():
        model = Post
        fields = ('title', 'body', 'read_duration', 'status', 'published_flag', 'favorite', 'categories', 'cover_image')#, 'new_tag' ]

    # def __init__(self, *args, **kwargs):
        # if kwaargs.get('instance'):
        #     initial = kwargs.setdefault('initial', {})
        #     if kwargs['instance'].category.all():
        #         initial['categories'] = kwargs['instance'].categories.all()[0]
        #     else:
        #         initial['categories'] = None
        # forms.ModelForm.__init__(self, *args, **kwargs)

    #     super().__init__(*args, **kwargs)
    #     self.fields['categories'].queryset = Category.objects.all()

# class Collaburation_keyForm(forms.ModelForm):
#     qs = Post.objects.filter()
#      = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your First Name" }))

# class Author_to_Collaburate(forms.ModelForm):
#     categories = forms.ModelMultipleChoiceField(queryset = Category.objects.all(), to_field_name="name", 
#     widget=forms.SelectMultiple(attrs={"class": "form-control col-md-3"}))
#     class Meta():
#         model = Post
#         fields = (title)

class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your Username" }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your First Name" }))
    last_name  = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your Last Name" }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your Email" }))
    # pass_one = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Password" }))
    # re_pass = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Repeat your password" }))
    # agree_term = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={"class": "agree-term" }))
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class RequestForm(forms.ModelForm):
    Selction = (
        ('Admin', 'Admin'),
        ('Others', 'Others'),
    )
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Title" }))
    message_to = forms.ModelChoiceField(required=False, queryset = User.objects.all(), to_field_name="username", widget=forms.Select( attrs={"class": "form-control form-control-lg" }))
    options  = forms.CharField(widget=forms.Select(choices=Selction, attrs={"class": "form-control form-control-lg", "id":"id_option_select", "data-role": "select-dropdown"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control form-control-lg", "placeholder": "Enter your message" }))
    class Meta():
        model = Author_request
        fields = ('title', 'message')

class Request_categoryForm(forms.ModelForm):
    category = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter New Category Name" }))
    class Meta():
        model = Author_request_category
        fields = ['category']

class ProfileForm(forms.ModelForm):
    SEX = (
    ('m', 'Male'),
    ('f', 'Female')
    )
    sex  = forms.CharField(required=False, label='What your gender?', widget=forms.Select(choices=SEX, attrs={"class": "form-control col-md-3"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control form-control-lg", "placeholder": "Enter your Biography"}))
    location  = forms.CharField(required=False, widget=forms.Select(choices=COUNTRY, attrs={"class": "form-control form-control-lg", 'data-role': "select-dropdown" }))
    cover_image = forms.ImageField(required=False, error_messages={'invalid':("Image files only")}, widget=forms.FileInput)
    birth_date = forms.CharField(required=False, label='Enter Date of birth?', widget=forms.DateInput(attrs={"class": "form-control form-control-lg", "type": "date", "placeholder": "Enter Date of birth?"}))
    whatsapp = forms.URLField(required=False, widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter your WhatsApp qr Address"}))
    linkedin = forms.URLField(required=False, widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter your LinkedIn url address"}))
    twitter = forms.URLField(required=False, widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter your twitter url address"}))
    github = forms.URLField(required=False, widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter your Github Address"}))
    visibility = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    remove_photo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
     
    class Meta():
        model = Profile
        fields = ('bio', 'cover_image', 'location', 'birth_date', 'sex', 'github', 'twitter', 'linkedin', 'whatsapp', 'visibility')

class Contact_usForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your Name"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your Email" }))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control form-control-lg", "placeholder": "Enter your message" }))
    class Meta():
        model = Contact_us
        fields = ('first_name', 'email', 'message')

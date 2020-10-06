from django.contrib.auth import (login as auth_login,  authenticate, logout)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import resolve
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
import random
import numpy as np
import hashlib
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
# from .forms import CommentForm, PostForms, ArticlesForm, BlogForm, PostForms2, TagForm
from .forms import CommentForm, CommentForm_author, PostForms, PostForms2, SignupForm, ProfileForm, RequestForm, Request_categoryForm, Contact_usForm
from .models import Post, Comment, Category, Tags, Newsletter_subcribers, Profile, Post_views, Author_request, Author_request_category, Contact_us, Collaburating_author, Post_history
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mebbscorner.tasks import notify_user2
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


site_initial = 'TTL'

def blog_index(request):
    posts = Post.objects.filter(published_flag=True, status='Ready').order_by('-created_on')
    context = {
        "bt_highlighted_index": True,
        "posts": posts,
    }
    return render(request, "blog_index.html", context)


@login_required
def collaburation_edit_blog(request, slug):
    cat = ''
    form = ''
    # articles_list = ''
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        selected_tags = ''
        if request.user.is_superuser:
            valid_post = PostForms(request.POST, request.FILES)
        else:
            valid_post = PostForms2(request.POST, request.FILES)
        if valid_post.is_valid():
            try:
                title=valid_post.cleaned_data['title']
                body=valid_post.cleaned_data['body']
                art_value = request.POST.getlist('categories')
                read_duration = valid_post.cleaned_data['read_duration']
                favorite = valid_post.cleaned_data['favorite']
                status = valid_post.cleaned_data['status']
                selected_tags = request.POST.get('tag_item')
                selected_tags = validate_tags(request,Tags,selected_tags)
                post.title = title
                post.body = body
                post.favorite=favorite
                post.read_duration=read_duration
                post.status= status
                remove_photo = valid_post.cleaned_data.get('remove_photo')
                image = valid_post.cleaned_data['cover_image']
                if image != post.cover_image:
                    if image != None:
                        post.cover_image = request.FILES['cover_image']
                if remove_photo:
                    post.cover_image = 'IMG_20200503_094546.jpg'
                post.slug = slugify(post.title)
                post.save()
                cat =  Category.objects.filter(posts__slug=slug)
                for ca in cat:
                    post.categories.remove(ca)
                for e in art_value:
                    cat = Category.objects.filter(name=e)
                    post.categories.add(*cat)
                
                _tag = Tags.objects.filter(tag__slug=slug)
                for ca in _tag:
                    post.new_tag.remove(ca)
                for e in selected_tags:
                    cat = Tags.objects.filter(name=e)
                    post.new_tag.add(*cat)
                Post_history.objects.create(
                    post=post,
                    author=request.user,
                    description= 'Edited',
                    state='Co Author'
                ).save()
                check_profile_state = Profile.objects.get(user=request.user)
                if check_profile_state.profile_complete != True:
                    status = 'Draft'
                    post.save()

                messages.success(request,'Post have been updated successfully!')
                if post.published_flag is True and post.status == 'Ready':
                    return redirect('blog:blog_detail', slug=post.slug)
                else:
                    return redirect('blog:pending_blog_detail', slug=post.slug)
            except Exception:
                messages.error(request, valid_post.errors)
    else:
        if request.user.is_superuser:
            form = PostForms(instance=post)
        else:
            form = PostForms2(instance=post)

        cat =  Category.objects.filter(posts__slug=slug)
        selected_tags = Tags.objects.filter(tag__slug=slug)
    content = {
        "bt_highlighted_add_blog": True,
        "form": form,
        "cat_selected": cat,
        "tags": selected_tags,
    }
    return render(request, 'dashboard_edit_post.html', content)

@login_required
def edit_blog(request, slug):
    cat = ''
    form = ''
    # articles_list = ''
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        selected_tags = ''
        if request.user.is_superuser:
            valid_post = PostForms(request.POST, request.FILES)
        else:
            valid_post = PostForms2(request.POST, request.FILES)
        if valid_post.is_valid():
            title=valid_post.cleaned_data['title']
            body=valid_post.cleaned_data['body']
            art_value = request.POST.getlist('categories')
            read_duration = valid_post.cleaned_data['read_duration']
            favorite = valid_post.cleaned_data['favorite']
            status = valid_post.cleaned_data['status']
            selected_tags = request.POST.get('tag_item')
            selected_tags = validate_tags(request,Tags,selected_tags)
            post.title = title
            post.body = body
            post.favorite=favorite
            post.read_duration=read_duration
            post.status= status
            remove_photo = valid_post.cleaned_data.get('remove_photo')
            image = valid_post.cleaned_data['cover_image']
            if image != post.cover_image:
                if image != None:
                    post.cover_image = request.FILES['cover_image']
            if remove_photo:
                post.cover_image = 'IMG_20200503_094546.jpg'
            post.slug = slugify(post.title)
            post.author = request.user; 
            post.save()
            check_profile_state = Profile.objects.get(user=request.user)
            if check_profile_state.profile_complete != True:
                status = 'Draft'
                post.save()

            cat =  Category.objects.filter(posts__slug=slug)
            for ca in cat:
                post.categories.remove(ca)
            for e in art_value:
                cat = Category.objects.filter(name=e)
                post.categories.add(*cat)
            
            _tag = Tags.objects.filter(tag__slug=slug)
            for ca in _tag:
                post.new_tag.remove(ca)
            for e in selected_tags:
                cat = Tags.objects.filter(name=e)
                post.new_tag.add(*cat)
            Post_history.objects.create(
                post=post,
                author=request.user,
                description= 'Edited',
                state='Main Author'
            ).save()
            messages.success(request,'Post have been updated successfully!')
            if post.published_flag is True and post.status == 'Ready':
                return redirect('blog:blog_detail', slug=post.slug)
            else:
                return redirect('blog:pending_blog_detail', slug=post.slug)
    else:
        if request.user.is_superuser:
            form = PostForms(instance=post)
        else:
            form = PostForms2(instance=post)
        cat =  Category.objects.filter(posts__slug=slug)
        selected_tags = Tags.objects.filter(tag__slug=slug)
    content = {
        "bt_highlighted_add_blog": True,
        "form": form,
        "cat_selected": cat,
        "tags": selected_tags,
    }
    return render(request, 'dashboard_edit_post.html', content)

@login_required
def blog(request):
    if request.user.is_superuser:
        form = PostForms()
    else:
        form = PostForms2()
    if request.method == 'POST':
        art_value = ''
        tag_value = ''
        if request.user.is_superuser:
            valid_post = PostForms(request.POST, request.FILES)
        else:
            valid_post = PostForms2(request.POST, request.FILES)
        if valid_post.is_valid():
            title=valid_post.cleaned_data['title']
            body=valid_post.cleaned_data['body']
            art_value = request.POST.getlist('categories')
            published_flag = valid_post.cleaned_data['published_flag']
            read_duration = valid_post.cleaned_data['read_duration']
            read_duration = valid_post.cleaned_data['cover_image']
            favorite = valid_post.cleaned_data['favorite']
            selected_tags = request.POST.get('tag_item')
            # selected_tags = validate_tags(request,Tags,selected_tags)
            new_post = Post.objects.create(
                title=title,
                body=body,
                published_flag=published_flag,
                favorite=favorite,
                read_duration=read_duration,
            )
            if image != None:
                new_post.cover_image = valid_post.cleaned_data['cover_image']
            new_post.slug = slugify(new_post.title)
            new_post.author = request.user
            new_post.save()
            # valid_post.save_m2m()
            for e in art_value:
                cat = Category.objects.filter(name=e)
                new_post.categories.add(*cat)
            for e in selected_tags:
                cat = Tags.objects.filter(name=e)
                new_post.new_tag.add(*cat)
            messages.success(request,'Post have been created successfully!')
            return redirect('blog_detail', slug=new_post.slug)

        else:
            messages.error(request, valid_post.errors)
    context = {
        "form": form,
    }
    return render(request, "blog.html", context)

@login_required
def add_category_request(request):
    category_updated = False
    message = 'Something went wrong'
    if request.is_ajax and request.method == 'POST':
        request_id = request.POST.get('list_id_category')
        request_category = request.POST.get('list_username_category')
        requested_check = Category.objects.filter(name__iexact=request_category).exists()
        author_to_category = Author_request_category.objects.filter(id=request_id, status__iexact='Pending').exists()
        update_cat = Author_request_category.objects.get(id=request_id)
        if requested_check is False and author_to_category:
            try:
                Category.objects.create(
                    name = str(update_cat.category),
                    added_by= update_cat.username
                ).save()
                update_cat.status = 'Completed'
                update_cat.approved_by = request.user
                update_cat.approved = True
                update_cat.modified_on = datetime.now()
                update_cat.save()
                category_updated = True
                message = 'Category has been saved'
            except Exception:
                category_updated = False
                message = 'Something went wrong'
        if requested_check:
            category_updated = False
            message = 'Data available in Category'
            update_cat.status = 'Completed'
            update_cat.approved_by = request.user
            update_cat.approved = True
            update_cat.save()

    data = {
        'category_registered': category_updated,
        'message': message
    }
    return JsonResponse(data)

@login_required
def add_category(request):
    ajax_request = False
    message = 'Something went wrong'
    if request.is_ajax and request.method == 'POST':
        category = request.POST.get('category')
        if category != '':
            post_check = Category.objects.filter(name=category).exists()
            if post_check is False:
                try:
                    Category.objects.create(
                        name = category,
                        added_by= request.user
                    ).save()
                    ajax_request = True
                    message = 'Category has been saved'
                except Exception:
                    ajax_request = False
                    message = 'Something went wrong'
        else:
            ajax_request = False
            message = 'Nice try'

    else:
        ajax_request = False
        message = 'Data already stored'

    data = {
            'category_registered': ajax_request,
            'message': message
    }
    return JsonResponse(data)
    
@login_required
def request_category(request):
    ajax_request = False
    if request.is_ajax and request.method == 'POST':
        valid_post_category = Request_categoryForm(request.POST, instance=request.user)
        if valid_post_category.is_valid():
            category = valid_post_category.cleaned_data["category"]
            query_check = Author_request_category.objects.filter(category=category, username=request.user).exists()
            if query_check is False:
                try:
                    Author_request_category.objects.create(
                        username = request.user,
                        category = category,
                        status='Pending' 
                    ).save()
                    ajax_request = True
                    message = 'Request has been submitted!'
                except Exception:
                    ajax_request = False
                    message = 'Something went wrong'
            else:
                ajax_request = False
                message = 'Data already stored'

    data = {
        'ajax_request': ajax_request,
        'message': message
    }
    return JsonResponse(data)

@login_required
def user_send_message(request):
    ajax_feedback = False
    message = 'Something went wrong'
    if request.is_ajax and request.method == 'POST':
        valid_post_request = RequestForm(request.POST, instance=request.user)
        if valid_post_request.is_valid():
            options = valid_post_request.cleaned_data["options"]
            try:
                if options == 'Admin':
                    title = valid_post_request.cleaned_data["title"]
                    message = valid_post_request.cleaned_data["message"]
                    new_request = Author_request.objects.create(
                    username = request.user,
                    title = title,
                    message = message,
                    weight = 'Heavy' 
                    )
                    new_request.encodededpk = urlsafe_base64_encode(force_bytes(new_request.id))
                    new_request.save()
                
                if options == 'Others':
                    title = valid_post_request.cleaned_data["title"]
                    message = valid_post_request.cleaned_data["message"]
                    receiver_query = valid_post_request.cleaned_data["message_to"]
                    receiver = User.objects.get(username=receiver_query)
                    new_request = Author_request.objects.create(
                    username = request.user,
                    title = title,
                    message = message,
                    weight = 'Flat',
                    message_to = receiver
                    )
                    new_request.encodededpk = urlsafe_base64_encode(force_bytes(new_request.id))
                    new_request.save()
                message = 'Message has been sent!'
                ajax_feedback = True
                RequestForm()

            except Exception:
                ajax_feedback = False
                message = 'Something went wrong'
        data = {
            'ajax_feedback': ajax_feedback,
            'message': message
    }
    return JsonResponse(data)


def add_newsletter_email(request):
    if request.is_ajax and request.method =='POST':
        email = request.POST.get('email_newsletter')
        email_check = Newsletter_subcribers.objects.filter(email__iexact=email).exists()
        if not email_check:
            try:
                new_email = Newsletter_subcribers.objects.create(
                    email = email
                )
                new_email.save()
                email_check = False
            except Exception:
                pass
    data = {
        'email_registered': email_check
    }
    return JsonResponse(data)

@login_required
def delete_blog(request, slug):  
    post = Post.objects.get(slug=slug)  
    post.delete()  
    messages.success(request, "The post has been delected Successfully")
    return HttpResponseRedirect("/blog/")

@login_required
def validate_tags(request, modelobject, selected_tags):
    selected_tags_final = []
    if selected_tags:
        selected_tag_two = selected_tags.split(',')
        buffer_list = []
        for aa in selected_tag_two:
            buffer_list.append(aa.rstrip())
        selected_tags = buffer_list
        tag_not_found = True
        for single_tag in selected_tags:
            checked_tag = modelobject.objects.filter(name=single_tag)
            if checked_tag.count() == 1:
                for existing_tag in checked_tag:
                    selected_tags_final.append(existing_tag)
            if checked_tag.count() == 0:
                modelobject(
                    name=single_tag,
                    added_by= request.user
                    ).save()
                selected_tags_final.append(single_tag)
        return selected_tags_final
    else:
        return selected_tags_final


def blog_category(request, category):
    post = Post.objects.filter(categories__name__contains=category).order_by(
        "-created_on")
    popular_post = Post.objects.filter(published_flag=True, status='Ready').order_by("-number_of_views")[:4]
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
            "category": category, 
            "posts": posts,
            "popular_post": popular_post
    }
    return render(request, "blog_category.html", context)

@login_required
def dashboard_pending_post(request):
    verified = False
    posts = Post.objects.all().order_by("published_flag")
    if request.user.is_superuser is True and request.user.is_authenticated:
        verified = True
    context = {
        "bt_highlighted_pending": True,
        "posts": posts,
        "verified": verified
    }
    return render(request, "dashboard_other_post.html", context)

@login_required
def add_post_request(request):
    ajax_request = False
    message = 'Something went wrong'
    if request.is_ajax and request.method == 'POST':
        request_id = request.POST.get('list_id')
        request_user = request.POST.get('list_author')
        requested_username = User.objects.get(username=request_user)
        post_check = Post.objects.filter(author=requested_username.id, id__iexact=request_id).exists()
        update_cat = Post.objects.get(id=request_id)
        if post_check and update_cat.published_flag is None:
            update_cat.published_flag = True
            update_cat.approved_by = request.user
            update_cat.save()
            ajax_request = True
            message = 'Request has been submitted!'

        else:
            ajax_request = False
            message = 'Something went wrong'
    data = {
        'ajax_request': ajax_request,
        'message': message
    }
    return JsonResponse(data)

@login_required
def verfiy_post_collaburation(request):
    post_updated = False
    message = 'Something went wrong'
    if request.is_ajax and request.method =='POST':
        try:
            request_id = request.POST.get('list_id')
            request_user = request.POST.get('list_author_in_request')
            requested_username = User.objects.get(username=request_user)
            post_check = Collaburating_author.objects.filter(author_in_request=requested_username.id, id__iexact=request_id).exists()
            update_colabo = Collaburating_author.objects.get(id=request_id)
            if post_check and update_colabo.status is False:
                update_colabo.status = True
                update_colabo.approved_on = datetime.now()
                update_colabo.approved_by = request.user
                update_colabo.save()
                post_updated = True
                message = 'Collaburation has been saved awaiting approval'
            else:
                post_updated = False
                message = 'Something went wrong'
        except Exception:
            post_updated = False
            message = 'Something went wrong'
   
    data = {
        'colabo_registered': post_updated,
        'message': message
    }
    return JsonResponse(data)

#1111
@login_required
def collaburation_handshake(request):
    collab_complete = False
    message = 'Something went wrong'
    if request.is_ajax and request.method == 'POST':
        try:
            title = request.POST.get('request_key')
            author = request.POST.get('request_author')
            check_one = Post.objects.filter(title__iexact=title).exists()
            check_two = User.objects.filter(username__iexact=author).exists()
            requestee = User.objects.get(username=request.user)
            post = Post.objects.get(title__iexact=title)
            requested_username = User.objects.get(username=author)
            post_check = Collaburating_author.objects.filter(author_in_request=requestee, post=post, requested_author=requested_username.id).exists()
            if check_one and check_two is True:
                if post_check is False:
                    try:
                        Collaburating_author.objects.create(
                            key = site_initial + hashify(title,str(datetime.now()),str(request.user)),
                            post = post,
                            author_in_request = request.user,
                            requested_author=requested_username,
                            approved_on = None
                        ).save()
                        collab_complete = True
                        message = 'Collaburation has been saved awaiting approval'
                    except Exception:
                        collab_complete = False
                        message = 'Something went wrong'
                else:
                    collab_complete = False
                    message = title,' collaburation already stored'
        except Exception:
            collab_complete = False
            message = 'Something went wrong'
    else:
        collab_complete = False
        message = 'Something went wrong'

    data = {
        'category_updated': collab_complete,
        'message': message
    }
    return JsonResponse(data)

@login_required
def request_key(request):
    collaburation_registered = False
    demanded_post = request.GET.get('requested_key_post', None)
    post = Post.objects.filter(title__iexact=demanded_post).exists()
    type(request.user)
    if post is True:
        try:
            Collaburating_author.objects.create(
                key = site_initial + hashify(demanded_post,str(datetime.now()),str(request.user)),
                post = Post.objects.get(title=demanded_post),
                author_in_request = request.user,
                approved_on = None
            ).save()
            collaburation_registered = True
        except Exception:
            collaburation_registered = False
    else:
        collaburation_registered = False

    data = {
    'collaburation_registered': collaburation_registered
    }
    return JsonResponse(data)

def hashify(post_title, date, user):
    result = ''
    srt2hash = post_title + date + user
    result = hashlib.md5(srt2hash.encode())
    return result.hexdigest()

def blog_author(request, author):
    author_id = User.objects.get(username=author)
    post = Post.objects.filter(published_flag=True, status='Ready', author=author_id).order_by("-created_on")
    popular_post = Post.objects.filter(published_flag=True, status='Ready').order_by("-number_of_views")[:4]
    
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        "author": author_id,
        "popular_post": popular_post,
        "category": author, 
        "posts": posts
    }
    return render(request, "blog_author.html", context)

def blog_tag(request, tag):
    posts = Post.objects.filter(new_tag__name__contains=tag).order_by(
        "-created_on")
    popular_post = Post.objects.filter(published_flag=True, status='Ready').order_by("-number_of_views")[:4]
    context = {
            "category": tag, 
            "posts": posts,
            "popular_post": popular_post,
    }
    return render(request, "blog_category.html", context)

def header_favorite(request):
    arr = np.array([])
    arr = np.append('a')
    # bb = np._dictlist({})
    # great_view = []
    # amount_present = Post.objects.all()
    # for p in amount_present:
    #     amount_viewed = Post_views.objects.filter(post_id=p.id).count()


def homepage_view(request):
    ran_cat_one_name = ''
    ran_cat_two_name = ''
    posts = Post.objects.filter(published_flag=True, status='Ready').order_by('-created_on')
    fav_post = Post.objects.filter(published_flag=True, status='Ready', favorite=True).order_by('-created_on')
    fav_post_solo = Post.objects.filter(published_flag=True, status='Ready', pk=1, favorite=True).order_by('-created_on')
    #Creating a favorite post
    if fav_post.count() > 1:
        fav_post_o = Post.objects.filter(published_flag=True, status='Ready', favorite=True)
        fp = []
        for p in fav_post_o:
            fp.append(p.id)
        fav_post_id = random.choice(fp)
        fav_post_solo = Post.objects.filter(published_flag=True, status='Ready', pk=fav_post_id)
    if fav_post.count() == 1:
        fav_post_solo = Post.objects.filter(published_flag=True, status='Ready', favorite=True)
    
    cat = Category.objects.all()
    cat_array = []
    for c in cat:
        cat_amount = Post.objects.filter(published_flag=True, status='Ready', categories__name__contains=c.name).count()
        if cat_amount > 0:
            cat_array.append(c.name)  
    if(len(cat_array) > 1):  # This will run when we have more posts belonging to the same category 
        ran_cat_one_name = random.choice(cat_array)
        ran_cat_two_name = random.choice(cat_array)
        while ran_cat_one_name == ran_cat_two_name:
            ran_cat_two_name = random.choice(cat_array)
        cat_one = Post.objects.filter(published_flag=True, status='Ready', categories__name__contains=ran_cat_one_name).order_by(
                "-created_on")[:3]
        cat_two = Post.objects.filter(published_flag=True, status='Ready', categories__name__contains=ran_cat_two_name).order_by(
                "-created_on")[:3]
        if(cat_two.count() > cat_one.count()):
            buffer_qs_one = cat_one
            buffer_name = ran_cat_one_name
            cat_one = cat_two
            cat_two = buffer_qs_one
            ran_cat_one_name = ran_cat_two_name
            ran_cat_two_name = buffer_name
    elif(len(cat_array) > 0):  # This will run when we have more posts belonging to the same category 
        ran_cat_one_name = cat_array[0]
        cat_one = Post.objects.filter(published_flag=True, status='Ready', categories__name__contains=cat_array[0]).order_by(
                "-created_on")[:3]
        cat_two = ''

    else: #This only works when you have only no m2m in category 
        ran_cat_one_name = ''
        ran_cat_two_name = ''
        cat_one = ''
        cat_two = ''
    
    recent = Post.objects.filter(published_flag=True, status='Ready').order_by(
                "-created_on")[:3]
    
    page = request.GET.get('page', 1)
    paginator = Paginator(recent, 3)
    try:
        recents = paginator.page(page)
    except PageNotAnInteger:
        recents = paginator.page(1)
    except EmptyPage:
        recents = paginator.page(paginator.num_pages)

    number_of_views_post('Ready')
    number_of_comments(request)
    featured_blog = Post.objects.filter(published_flag=True, status='Ready').order_by("-number_of_views","-number_of_comments")[:2]
    featured_blog_single = featured_blog.first()
    popular_post = Post.objects.filter(published_flag=True, status='Ready').order_by("-number_of_views")[:4]
    trending_post = Post.objects.filter(published_flag=True, status='Ready', favorite=True).order_by("-number_of_views")[:4]
    context = {
        "bt_highlighted_home": True,
        "posts": posts,
        "popular_post": popular_post,
        "cat_one_posts": cat_one,
        "recents": recents,
        "ran_cat_one_name": ran_cat_one_name,
        "cat_two_posts": cat_two,
        "ran_cat_two_name": ran_cat_two_name,
        "fav_posts": fav_post,
        "fav_post_solo": fav_post_solo,
        "trending_post": trending_post,
        "featured_blog": featured_blog,
        "featured_blog_single": featured_blog_single
    }
    return render(request, 'home.html', context)

def blog_index_search(request):
    if request.method == 'POST':
        keyword = request.POST.get('search_word')
        status = "Ready"
        posts = Post.objects.filter(published_flag=True, status=status, body__icontains=keyword) | Post.objects.filter(published_flag=True, status='Ready', title__icontains=keyword) | Post.objects.filter(published_flag=True, status='Ready', categories__name__icontains=keyword)
    context = {
        'posts': posts,
        'title': keyword
    }
    return render(request, 'search_result.html', context)

def blog_index_searched(request, keyword):
    posts = Post.objects.filter(body__contains=keyword)
    context = {
        'post': posts
    }
    return render(request, 'search_result.html', context)

@login_required
def dashboard_add_post(request, author):
    if request.method == 'POST':
        art_value = ''
        tag_value = ''
        if request.user.is_superuser:
            valid_post = PostForms(request.POST, request.FILES)
        else:
            valid_post = PostForms2(request.POST, request.FILES)

        if valid_post.is_valid():
            try:
                title=valid_post.cleaned_data['title']
                body=valid_post.cleaned_data['body']
                art_value = request.POST.getlist('categories')
                status = valid_post.cleaned_data['status']
                read_duration = valid_post.cleaned_data['read_duration']
                favorite = valid_post.cleaned_data['favorite']
                image = valid_post.cleaned_data['cover_image']
                selected_tags = request.POST.get('tag_item')
                selected_tags = validate_tags(request, Tags,selected_tags)
                new_post = Post.objects.create(
                    title=title,
                    body=body,
                    status=status,
                    favorite=favorite,
                    read_duration=read_duration,
                )
                if image != None:
                    new_post.cover_image = request.FILES['cover_image']
                new_post.slug = slugify(new_post.title)
                new_post.author = request.user
                new_post.save()
                check_profile_state = Profile.objects.get(user=request.user)
                if check_profile_state.profile_complete != True:
                    status = 'Draft'
                    new_post.save()

                for e in art_value:
                    cat = Category.objects.filter(name=e)
                    new_post.categories.add(*cat)
                for e in selected_tags:
                    cat = Tags.objects.filter(name=e)
                    new_post.new_tag.add(*cat)
                Post_history.objects.create(
                    post=new_post.id,
                    author=request.user,
                    description= 'Created',
                    state='Main Author'
                ).save()
                messages.success(request,'Post have been created successfully!')
                if post.published_flag is True:
                    return redirect('blog:blog_detail', slug=post.slug)
                else:
                    return redirect('blog:pending_blog_detail', slug=post.slug)
            except Exception:
                pass
        else:
            messages.error(request, valid_post.errors)
    if request.user.is_superuser:
        form = PostForms()
    else:
        form = PostForms2()
    context = {
        "bt_highlighted_add_post": True,
        "form": form,
        "author": author
    }
    return render(request, 'dashboard_add_post.html', context) 

@login_required
def dashboard_request(request, author):
    encap = ''
    request_list = ''
    if request.user.is_superuser is True:
        form = Author_request.objects.all().order_by("-created_on")
        form_cat = Author_request_category.objects.all().order_by("-created_on")
        request_key = Collaburating_author.objects.all().order_by("-created_on")
        request_list = Post.objects.filter(author=request.user)
        encap = True
        form_message = ''
    else:
        form = Author_request.objects.filter(username=request.user).order_by("-created_on")
        request_key = Collaburating_author.objects.filter(author_in_request=request.user).order_by("-created_on")
        form_message = RequestForm(instance=request.user)
        form_cat = Request_categoryForm(instance=request.user)
        request_list = Post.objects.filter(author=request.user)
        encap = False

    context = {
        "bt_highlighted_dashboard_request": True,
        "author": author,  
        "form": form,
        "form_cat": form_cat,
        "form_message": form_message,
        "encap": encap,
        "request_list": request_list,
        "request_key": request_key
    }
    return render(request, 'dashboard_request.html', context)

@login_required
def dashboard_messaging(request, author):
    encap = ''
    form_message = RequestForm(instance=request.user)
    if request.user.is_superuser is True:
        encap = True
        form = Author_request.objects.filter(weight='Heavy').order_by("-created_on") | Author_request.objects.filter(message_to=request.user).order_by("-created_on")
        request_list = Post.objects.filter(author=request.user)
    else:
        encap = False
        form = Author_request.objects.filter(weight='Flat', message_to=request.user).order_by("-created_on")
        request_list = Post.objects.filter(author=request.user)
    context = {
      "bt_highlighted_messaging": True,
      "author": author,  
      "form": form,
      "encap": encap,
      "request_list": request_list,
      "form_message": form_message,
    }
    return render(request, 'dashboard_messaging.html', context)

@login_required
def dashboard_opened_message(request, author, uidb64):
    authorized = False
    if request.user.is_authenticated:
        selected_message = Author_request.objects.get(encodededpk=uidb64)
        if selected_message.weight == 'Heavy' and request.user.is_superuser:
            opened_selected_message = Author_request.objects.get(encodededpk=uidb64)
            authorized = True
            if opened_selected_message.markas_read is False:
                opened_selected_message.markas_read = True
                opened_selected_message.approved_by = request.user
                opened_selected_message.save()
        elif selected_message.weight == 'Flat':
            opened_selected_message = Author_request.objects.get(encodededpk=uidb64)
            authorized = True
            if opened_selected_message.markas_read is False:
                opened_selected_message.markas_read = True
                opened_selected_message.approved_by = request.user
                opened_selected_message.save()
        else:
            authorized = False
            opened_selected_message = ''
    context = {
        'selected_message': opened_selected_message,
        'bt_highlighted_messaging': True,
    }
    return render(request, 'dashboard_opened_message.html', context)

def blog_contact(request):
    form = Contact_usForm()
    if request.method == 'POST':
        try:
            check_form = Contact_usForm(request.POST)
            if check_form.is_valid():
                check_form.save()
                form = Contact_usForm()
                messages.success(request, 'Your message has been delivered successfully')
        except Exception as identifier:
            pass
    context = {
        'bt_highlighte_contact': True,
        'form': form
    }
    return render(request, 'blog_contact.html', context)

@login_required
def dashboard_view_post(request, author):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by('-created_on')
    context = {
        "bt_highlighted_view_post": True,
        "posts": posts,
        "author": author
    }
    return render(request, 'dashboard_view_post.html', context)

@login_required
def dashboard_view_post_edit(request, author):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by('-created_on')
    context = {
        "bt_highlighted_edit": True,
        "posts": posts,
        "author": author
    }
    return render(request, 'dashboard_view_post_edit.html', context)

#111
@login_required
def dashboard_collabutation_view(request, author):
    if request.user.is_authenticated:
        try:
            _qs = User.objects.get(username=author)
            posts = Collaburating_author.objects.filter(requested_author=_qs).order_by('-created_on')
            post_list = []
            for pl_qs in posts:
                post_list.append(pl_qs.post)
            posts = Post.objects.filter(title__in=post_list)
        except Exception:
            pass
    context = {
        "bt_highlighted_dashboard_collabutation_view": True,
        "posts": posts,
        "author": author
    }
    return render(request, 'dashboard_view_post_collaburation.html', context)

@login_required
def dashboard_authors(request):
    if request.user.is_authenticated:
        number_of_views_author(request)
        number_of_posts()
        author = User.objects.all().order_by('-is_superuser')
        login_user = User.objects.get(username=request.user)
        context = {
            "bt_highlighted_dashboard_authors": True,
            "authors": author,
            "login_user": str(login_user.username),
        }
    return render(request, 'dashboard_authors.html', context)



# @transaction.atomic
@login_required
def dashboard_profile(request, author):
    form = SignupForm(instance=request.user)
    form_two = ProfileForm(instance=request.user.profile)
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                update_user = User.objects.get(id=request.user.id)
                update_user_two = Profile.objects.get(user_id=request.user.id)
                valid_form = SignupForm(request.POST, instance=request.user)
                valid_form_two = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
                if valid_form.is_valid() and valid_form_two.is_valid():
                    update_user.username = valid_form.cleaned_data['username']
                    update_user.email = valid_form.cleaned_data['email']
                    update_user.first_name = valid_form.cleaned_data['first_name']
                    update_user.last_name = valid_form.cleaned_data['last_name']
                    update_user.save()
                    update_user_two.location = valid_form_two.cleaned_data['location']
                    update_user_two.birth_date = valid_form_two.cleaned_data['birth_date']
                    update_user_two.bio = valid_form_two.cleaned_data['bio']
                    update_user_two.linkedin = valid_form_two.cleaned_data['linkedin']
                    update_user_two.twitter = valid_form_two.cleaned_data['twitter']
                    update_user_two.github = valid_form_two.cleaned_data['github']
                    update_user_two.whatsapp = valid_form_two.cleaned_data['whatsapp']
                    update_user_two.visibility = valid_form_two.cleaned_data['visibility']
                    update_user_two.sex = valid_form_two.cleaned_data['sex']
                    remove_photo = valid_form_two.cleaned_data.get('remove_photo')
                    image = valid_form_two.cleaned_data['cover_image']
                    if image != update_user_two.cover_image:
                        update_user_two.cover_image = request.FILES['cover_image']
                    if remove_photo:
                        update_user_two.cover_image = 'default_image.jpg'
                    update_user_two.save()

                    if update_user.username != None and update_user.first_name != None and update_user.last_name != None and update_user_two.location != None and update_user_two.bio !=None:
                        update_user_two.profile_complete = True
                        update_user_two.save()
                    else:
                        update_user_two.profile_complete = False
                        update_user_two.save()


                    messages.success(request, "Your account has been successfully updated")
                    return redirect('blog:dashboard_home', request.user)
                else:
                    messages.error(request, "Something went wrong")
                    form = SignupForm(instance=request.user)
                    form_two = ProfileForm(instance=request.user.profile)
            except ValidationError as e:
                messages.error(request, ValidationError.str(e))
            except ValueError as e:
                update_user_two.cover_image = ''
        else:
            form = SignupForm(instance=request.user)
            form_two = ProfileForm(instance=request.user.profile)
        context = {
            "bt_highlighted_profile": True,
            "form": form,
            "form_two": form_two,
        }
        return render(request, 'dashboard_profile.html', context)

@login_required
def dashboard_home(request, author):
    author_instance = User.objects.get(username=author)
    user_gist = User.objects.filter(username=author_instance)
    profile_gist = Profile.objects.get(user=author_instance)
    collab_count = Collaburating_author.objects.filter(author_in_request=author_instance)
    context = {
        "collab_count": collab_count,
        "user_gist": user_gist,
        "profile_gist": profile_gist,
        "bt_highlighted_home": True,
        "author": author
    }
    return render(request, 'dashboard_home.html', context)

def number_of_views_post(status):
    ping_user_id = Post.objects.filter(published_flag=True, status=status)
    for p in ping_user_id:
        view_post = Post_views.objects.filter(post=p.id).count()
        no_of_view = Post.objects.get(pk=p.id)
        no_of_view.number_of_views = view_post
        no_of_view.save()

def record_view(request, post_id):
    view_post = get_object_or_404(Post, pk=post_id)
    if not Post_views.objects.filter(
                    post=view_post,
                    session=request.session.session_key):
        view = Post_views(
            post=view_post,
            ip=request.META['REMOTE_ADDR'],
            session=request.session.session_key)
        view.save()

def number_of_comments(request):
    try:
        post_qs = Post.objects.filter(published_flag=True, status='Ready')
        for pm in post_qs:
            comment_ammount = Comment.objects.filter(post=pm.id).count()
            post_view = Post.objects.get(id=pm.id)
            post_view.number_of_comments = comment_ammount
            post_view.save()
    except Exception:
        pass
        

def number_of_post_profile_single(request, post_user):
    try:
        view_post = Post.objects.filter(published_flag=True, status='Ready', author=post_user).count()
        edit_views = Profile.objects.get(user_id=post_user)
        edit_views.number_of_post = view_post
        edit_views.save()
    except Exception:
        pass

def number_of_posts():
    try:
        ping_user_id = Post.objects.filter(published_flag=True, status='Ready')
        for p in ping_user_id:
            view_post = Post.objects.filter(published_flag=True, status='Ready',author=p.author_id).count()
            edit_views = Profile.objects.get(user_id=p.author_id)
            edit_views.number_of_post = view_post
            edit_views.save()
    except Exception:
        pass

def number_of_views_author(request):
    try:
        ping_user_id = Post.objects.filter(published_flag=True, status='Ready')
        for p in ping_user_id:
            view_post = Post_views.objects.filter(post=p.id).count()
            edit_views = Profile.objects.get(user_id=p.author_id)
            edit_views.number_of_views = view_post
            edit_views.save()
    except Exception:
        pass

def popular_views(request):
    popular = Post.objects.filter(published_flag=True, status='Ready').order_by("-number_of_views")
    page = request.GET.get('page', 1)
    paginator = Paginator(popular, 2)
    try:
        popular_post = paginator.page(page)
    except PageNotAnInteger:
        popular_post = paginator.page(1)
    except EmptyPage:
        popular_post = paginator.page(paginator.num_pages)
    context = {
        'posts': popular_post
    }
    return render(request, 'blog_popular.html', context)


def dashboard_collaburation(request, author):
    request_list = Post.objects.filter(author=request.user)
    author_list = User.objects.exclude(username=request.user)
    context = {
      "request_list": request_list,
      "author_list": author_list,
      "author": author,
    }
    return render(request, 'dashboard_collaburation.html', context)

def blog_detail(request, slug):
    edit_post = False
    comment_form = ''
    post = get_object_or_404(Post, slug=slug, published_flag=True, status='Ready')
    collab_author = Collaburating_author.objects.filter(post=post)
    post2 = Post.objects.get(slug=slug)
    commentable = post2.published_flag
    number_of_posts()
    number_of_views_post('Ready')
    record_view(request, post2.id)
    comments = post2.comments.filter(active=True, parent__isnull=True)
    comment_total = post2.comments.filter(active=True).count()
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                check_up = Collaburating_author.objects.filter(post=post2, requested_author=request.user).exists()
                comment_form = CommentForm_author(data=request.POST)
                if comment_form.is_valid():
                    parent_obj = None
                    try:
                        parent_id = int(request.POST.get('parent_id'))
                    except:
                        parent_id = None
                    if parent_id:
                        parent_obj = Comment.objects.get(id=parent_id)
                        if parent_obj:
                            replay_comment = Comment.objects.create(
                                body = '@<strong>%s:</strong> %s'%(request.POST.get('parent_name'), comment_form.cleaned_data['body']),
                                post = post
                            )
                            if post.author == request.user:
                                replay_comment.name = request.user.get_full_name()
                                replay_comment.email = request.user.email
                                replay_comment.parent = parent_obj
                                replay_comment.author_voice = True
                                replay_comment.active_writer_inst = request.user
                                replay_comment.save()
                            elif check_up:
                                replay_comment.name = request.user.get_full_name()
                                replay_comment.email = request.user.email
                                replay_comment.parent = parent_obj
                                replay_comment.co_author_voice = True
                                replay_comment.active_writer_inst = request.user
                                replay_comment.save()
                            else:
                                replay_comment.name = request.user.get_full_name()
                                replay_comment.email = request.user.email
                                replay_comment.parent = parent_obj
                                replay_comment.active_writer = True
                                replay_comment.active_writer_inst = request.user
                                replay_comment.save()
                    else:
                        new_comment = Comment.objects.create(
                            body = comment_form.cleaned_data['body'],
                            post = post
                            )
                        if post.author == request.user:
                            new_comment.name = request.user.get_full_name()
                            new_comment.email = request.user.email
                            new_comment.author_voice = True
                            new_comment.active_writer_inst = request.user
                            new_comment.save()
                        
                        elif check_up:
                            new_comment.name = request.user.get_full_name()
                            new_comment.email = request.user.email
                            new_comment.co_author_voice = True
                            new_comment.active_writer_inst = request.user
                            new_comment.save()

                        else:
                            new_comment.name = request.user.get_full_name()
                            new_comment.email = request.user.email
                            new_comment.active_writer = True
                            new_comment.active_writer_inst = request.user
                            new_comment.save()
                    messages.success(request, "The comment has been posted successfully")
                    # return HttpResponseRedirect(post.get_absolute_url())
                    return redirect('blog:blog_detail', slug=post.slug)

            else:
                comment_form = CommentForm(data=request.POST)
                if comment_form.is_valid():
                    parent_obj = None
                    # get parent comment id from hidden input
                    try:
                        # id integer e.g. 15
                        parent_id = int(request.POST.get('parent_id'))
                    except:
                        parent_id = None
                    # if parent_id has been submitted get parent_obj id
                    if parent_id:
                        parent_obj = Comment.objects.get(id=parent_id)
                        # if parent object exist
                        if parent_obj:
                            # create replay comment object
                            replay_comment = comment_form.save(commit=False)
                            replay_comment.body = '@%s %s'%(request.POST.get('parent_name'), comment_form.cleaned_data['body'])
                            # assign parent_obj to replay comment
                            replay_comment.parent = parent_obj
                    # normal comment
                    # create comment object but do not save to database
                    new_comment = comment_form.save(commit=False)
                    # assign ship to the comment
                    new_comment.post = post
                    # save
                    new_comment.save()
                    messages.success(request, "The comment has been posted successfully")
                    # return HttpResponseRedirect(post.get_absolute_url())
                    return redirect('blog:blog_detail', slug=post.slug)
        except Exception:
            pass

    else:
        if request.user.is_authenticated:
            comment_form = CommentForm_author()
        else:
            comment_form = CommentForm()

    if request.user.is_authenticated:
        if(request.user == post.author):
            edit_post = True
        else:
            edit_post = False
    popular_post = Post.objects.filter(published_flag=True, status='Ready').order_by("-number_of_views")[:4]
    profile_gist = Profile.objects.get(user=post.author)
    context = {
        'collab_author': collab_author,
        'popular_post': popular_post,
        'comment_total': comment_total,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'edit_post': edit_post,
        'commentable': commentable,
        'profile_gist': profile_gist

        }
    return render(request, "blog_detail.html", context)

def blog_detail_legal(request, slug):
    post = get_object_or_404(Post, slug=slug)
    edit_post = False
    post2 = Post.objects.get(slug=slug)
    number_of_posts()
    number_of_views_post('Legal')
    record_view(request, post2.id)

    if request.user.is_authenticated:
        if(request.user == post.author):
            edit_post = True
        else:
            edit_post = False

    context = {
        'post': post,
        'edit_post': edit_post,
        }
    return render(request, "pending_blog_detail.html", context)

@login_required
def pending_blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    edit_post = False
    if request.user.is_authenticated:
        if(request.user == post.author):
            edit_post = True
        else:
            edit_post = False

    context = {
        'post': post,
        'edit_post': edit_post,
        }
    return render(request, "pending_blog_detail.html", context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
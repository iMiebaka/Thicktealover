from django.shortcuts import render
from django.contrib.auth import (login as auth_login,  authenticate, logout)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
import re
import string
import hashlib
from datetime import datetime
import time 

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.views.generic import View, UpdateView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import render, get_object_or_404, redirect
from blog.forms import CommentForm, PostForms2
from .forms import PasswordResetForm, PasswordResetConfirmViewForm
from blog.models import Post, Comment, Category, Tags


def login(request):
    if request.user.is_authenticated:
        messages.error(request,'Please logout first')
        return redirect('blog:dashboard_home', author=request.user)
    else:
        if request.method == 'POST':
            username = request.POST['your_name']
            raw_password = request.POST['your_pass']
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Logged in")
                return redirect('blog:dashboard_home', author=user)
            else:
                messages.error(request, 'Ops')
        else:
            pass
    # print(urlsafe_base64_encode(force_bytes(request.user.pk)))
    # print(default_token_generator.make_token(request.user))
    return render(request, 'login.html', {"bt_highlighte_signing": True})


def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        raw_password = request.POST['pass']
        email_address = request.POST['email']
        _available = User.objects.filter(username__iexact=username).exists() | User.objects.filter(email__iexact=email_address).exists() 
        if raw_password == request.POST['re_pass'] and _available == False:
            if _available == False:
                user = User.objects.create_user(
                    username, 
                    email_address,
                    raw_password
                )
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.is_active = False
                no_user = User.objects.all().count()
                if no_user == 0:
                    user.is_superuser = True
                user.save()

                subject = 'Activate Your TTL Account'
                email_template_name = "validate_email.txt"
                c = {
                    "email":user.email,
                    'domain':get_current_site(request),
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    messages.success(request, ('Please Confirm your email to complete registration.'))
                    corespondent = redirect("accounts:email_verification_sent")
                    srt2hash = str(datetime.now()) + 'Engaged'
                    key = hashlib.md5(srt2hash.encode()).hexdigest()
                    corespondent.set_cookie('TTL_EV', key , max_age=7200)
                    return corespondent

                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                # auth_login(request, user)
                # messages.success(request, "Your account has been successfully created")
            else:
                messages.error(request, "Username is unavaliable")
    return render(request, 'signup.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out")
        return HttpResponseRedirect("/")

def logout_to_login_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out")
        return redirect('accounts:login')

def password_strenght(request):
    ajax_request = False
    message = ''
    if request.method == 'POST' and request.is_ajax:
        password = request.POST.get('password')
        if bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&]).{8,30})', password)) == True:
            message = 'Password Strength 5/5'
            ajax_request = True
        elif bool(re.match('((\d*)([a-z]*)([A-Z]*).{8,30})', password)) == True:
            message = 'Password Strength 4/5'
            ajax_request = True
        elif bool(re.match('((\d*)([a-z]*).{8,30})', password)) == True:
            message = 'Password Strength 3/5'
            ajax_request = True
        elif bool(re.match('(([a-z]*).{8,30})', password)) == True:
            message = 'Password Strength 2/5'
            ajax_request = True
        elif bool(re.match('(([a-z]*).{1,30})', password)) == True:
            message = 'Password Strength 2/5'
            ajax_request = True
        else:
            message = 'Password Strength 1/5'
            ajax_request = True
    data = {
        'message' : message,
        'ajax_request': ajax_request
    }
    return JsonResponse(data)

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def change_password_from_email(request):
    form = PasswordResetConfirmViewForm()
    context = {
        'form': form
    }
    return render (request, 'password_reset_confirm.html', context)

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            try:
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "password_reset_email.txt"
                        c = {
                            "email":user.email,
                            'domain':get_current_site(request),
                            'site_name': 'TTL',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'support@thicktealover.com' , [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        messages.success(request, "Reset link sent to email")
                        corespondent = redirect("accounts:custom_password_reset_done")
                        srt2hash = str(datetime.now()) + 'Engaged'
                        key = hashlib.md5(srt2hash.encode()).hexdigest()
                        corespondent.set_cookie('TTL_PSR', key , max_age=7200)
                        return corespondent
                else:
                    messages.error(request, 'Email is not registered to this site')
            except:
                pass
    password_reset_form = PasswordResetForm()
    context = { "password_reset_form":password_reset_form }
    corespondent = render(request, "reset_password.html", context)
    return corespondent
    # return render(request, "reset_password.html", context)

def custom_password_reset_done(request):
    if request.COOKIES.get('TTL_PSR') is None:
        messages.error(request, 'Your previous request was incomplete')
        return redirect("blog:homepage_view")
    return render(request, 'password_reset_link.html')

def custom_password_reset_done_complete(request):
    corespondent = render(request, 'password_reset_complete.html')
    if request.COOKIES.get('TTL_PSR'):
        srt2hash = str(datetime.now()) + 'Terminate'
        key = hashlib.md5(srt2hash.encode()).hexdigest()
        corespondent.set_cookie('TTL_PSR', key, max_age=60)
        return corespondent
    else:
        messages.error(request, 'Your previous request was incomplete')
        return redirect("accounts:login")

def email_verification_sent(request):
    corespondent = render(request, 'verify_email_complete.html')
    if request.COOKIES.get('TTL_EV'):
        srt2hash = str(datetime.now()) + 'Terminate'
        key = hashlib.md5(srt2hash.encode()).hexdigest()
        corespondent.set_cookie('TTL_EV', key , max_age=60)
        return corespondent
    else:
        messages.error(request, 'Your previous request was incomplete')
        return redirect("blog:homepage_view")

def validate_username_signup(request):
    username = request.GET.get('username', None)
    data = {
        'user_is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def validate_email_signup(request):
    email = request.GET.get('email', None)
    data = {
        'email_is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

def ActivateAccount(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        auth_login(request, user)
        messages.success(request, ('Your account have been confirmed.'))
        return HttpResponseRedirect("/")
    else:
        messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
        return HttpResponseRedirect("/")

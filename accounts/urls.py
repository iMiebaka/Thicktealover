from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout_view"),    
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('ajax/password_strenght/', views.password_strenght, name='password_strenght'),
    path('ajax/validate_username_signup/', views.validate_username_signup, name='validate_username_signup'),
    path('ajax/validate_email_signup/', views.validate_email_signup, name='validate_email_signup'),
    path("reset_password/", views.password_reset_request, name="password_reset"),
    path("verify_account/", views.verify_account, name="verify_account"),
    path('reset_password_sent', views.custom_password_reset_done, name='custom_password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password_reset_complete/', views.custom_password_reset_done_complete, name='custom_password_reset_done_complete'),
    path('email_verification_sent/', views.email_verification_sent, name='email_verification_sent'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount, name='ActivateAccount'),
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
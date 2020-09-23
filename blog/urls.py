from django.urls import path
from django.contrib.auth import views as auth_views
# from django.contrib.auth import views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'
urlpatterns = [
    # path("articles_check/", views.articles_display, name="articles_display"),

    path('', views.homepage_view, name='homepage_view'),
    path('blogs/', views.blog_index, name="blog_index"),
    path('search_result/', views.blog_index_search, name="blog_index_search"),
    path('search_results/', views.blog_index_searched, name="blog_index_searched"),
    path('popular/', views.popular_views, name="popular_views"),
    path("new/", views.blog, name="blog"),
    path("contact-us/", views.blog_contact, name="blog_contact"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("legal/<slug:slug>/", views.blog_detail_legal, name="blog_detail_legal"),
    path("pending/<slug:slug>/", views.pending_blog_detail, name="pending_blog_detail"),
    path("articles_list/<category>/", views.blog_category, name="blog_category"),
    path("tags_list/<tag>/", views.blog_tag, name="blog_tag"),
    path("dashboard/authors/", views.dashboard_authors, name="dashboard_authors"),
    path("dashboard/pending/", views.dashboard_pending_post, name="dashboard_pending_post"),
    path("author/<author>/", views.blog_author, name="blog_author"),
    path("dashboard/<author>/", views.dashboard_home, name="dashboard_home"),
    path("dashboard/<author>/messaging", views.dashboard_messaging, name="dashboard_messaging"),
    path("dashboard/<author>/request", views.dashboard_request, name="dashboard_request"),
    path("dashboard/<author>/collaburation", views.dashboard_collaburation, name="dashboard_collaburation"),
    path("dashboard/<author>/new", views.dashboard_add_post, name="dashboard_add_post"),
    path("dashboard/<author>/posts", views.dashboard_view_post, name="dashboard_view_post"),
    path("dashboard/<author>/edit", views.dashboard_view_post_edit, name="dashboard_view_post_edit"),
    path("dashboard/<author>/posts-collaburation", views.dashboard_collabutation_view, name="dashboard_collabutation_view"),
    path("dashboard/<author>/profile", views.dashboard_profile, name="dashboard_profile"),
    path("dashboard/<slug:slug>/edit/", views.edit_blog, name="edit_blog"), 
    path("dashboard/collaburation/<slug:slug>/edit/", views.collaburation_edit_blog, name="collaburation_edit_blog"), 
    path("<slug:slug>/delete/", views.delete_blog, name='delete_blog'), 
    path("ajax/addnewsletter/", views.add_newsletter_email, name='add_newsletter_email'),
    path("ajax/add_category_request/", views.add_category_request, name='add_category_request'),
    path("ajax/request_key/", views.request_key, name='request_key'),
    path("ajax/verfiy_post_collaburation/", views.verfiy_post_collaburation, name='verfiy_post_collaburation'),
    path("ajax/collaburation_handshake/", views.collaburation_handshake, name='collaburation_handshake'),
    path("ajax/request_category/", views.request_category, name='request_category'),
    path("ajax/user_send_message/", views.user_send_message, name='user_send_message'),
    # path("ajax/user_send_message_other/", views.user_send_message_other, name='user_send_message_other'),
    # path("ajax/user_send_message_admin/", views.user_send_message_admin, name='user_send_message_admin'),
    path("ajax/add_category/", views.add_category, name='add_category'),
    path("ajax/verify_post/", views.add_post_request, name='add_post_request'),
    # path("articles/<slug:slug>/", views.category_archive, name='category_archive'),
    # path("<int:pk>/", views.blog_detail, name="blog_detail"),
    # path("<int:pk>/edit/", views.edit_blog, name="edit_blog"),
    # path("<int:pk>/delete/", views.delete_blog, name='delete_blog'),
    # path("add_comment/<int:pk>/", views.add_comment, name="add_comment"),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
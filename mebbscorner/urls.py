from django.contrib import admin
from django.urls import path, include
from .tasks import notify_user
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# from my_app.views import (
#     indexView,
#     postFriend,
#     checkNickName,
# )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('blog.urls',namespace="blog")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path("accounts/", include('accounts.urls', namespace="accounts")),
    # path('accounts/', include('django.contrib.auth.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
# notify_user(repeat=10, repeat_until=None)
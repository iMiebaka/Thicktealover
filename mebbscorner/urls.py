from django.contrib import admin
from django.urls import path, include
from .tasks import notify_user
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import StaticSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    # 'article': PostSitemap,
    'static': StaticSitemap
    }

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('blog.urls',namespace="blog")),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path("accounts/", include('accounts.urls', namespace="accounts")),
    # path('accounts/', include('django.contrib.auth.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
# notify_user(repeat=10, repeat_until=None)
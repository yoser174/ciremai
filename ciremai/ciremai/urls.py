from django.conf import settings
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve


urlpatterns = [
    url(r'^select2/', include('django_select2.urls')),
    
    url(r'^admin/', admin.site.urls),
    url(r'^billing/', include('billing.urls')),
    # midleware - Worklist - entry result - validate
    url(r'^middleware/', include('middleware.urls')),
    
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT})
    ]
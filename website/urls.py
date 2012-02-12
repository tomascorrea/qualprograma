from django.conf.urls.defaults import *

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings


from core.views import home

urlpatterns = patterns('',
    url(r'^$', home, name="home"),
    (r'^busca/', include('busca.urls')),
    (r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

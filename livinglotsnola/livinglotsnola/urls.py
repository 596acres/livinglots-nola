from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import autocomplete_light

autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
                     show_indexes=True)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    # Activity stream urls
    url('^activity/', include('actstream.urls')),
    url('^activity-stream/', include('inplace_activity_stream.urls')),

    # Django.js
    url(r'^djangojs/', include('djangojs.urls')),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # Autocomplete
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # FeinCMS
    url(r'', include('feincms.urls')),
)

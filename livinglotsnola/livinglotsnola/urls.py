from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import autocomplete_light
import external_data_sync

from registration.forms import AuthenticationForm

autocomplete_light.autodiscover()
external_data_sync.autodiscover()
admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
                     show_indexes=True)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url('^parcels/', include('noladata.parcels.urls')),
    )

urlpatterns += patterns('',
    # Living Lots
    url(r'^lots/(?P<pk>\d+)/content/', include('usercontent.urls', 'usercontent')),
    url(r'^lots/(?P<pk>\d+)/grow-community/', include('organize.urls', 'organize')),
    url(r'^lots/', include('lots.urls', 'lots')),

    # NOLA data
    url('^councildistricts/', include('noladata.councildistricts.urls')),
    url('^zipcodes/', include('noladata.zipcodes.urls')),

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

    # Auth
    url(r'^login/', 'django.contrib.auth.views.login', {
        'authentication_form': AuthenticationForm,
    }),

    # FeinCMS
    url(r'', include('feincms.urls')),
)


from django.shortcuts import render

from feincms.module.page.models import Page


def page_not_found(request, template_name='404.html'):
    page = Page.objects.best_match_for_path(request.path)
    return render(request, template_name, {'feincms_page': page}, status=404)


def error_handler(request, template_name='500.html'):
    page = Page.objects.best_match_for_path(request.path)
    return render(request, template_name, {'feincms_page': page}, status=500)


handler404 = page_not_found
handler500 = error_handler

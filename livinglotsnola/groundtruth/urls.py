from django.conf.urls import patterns, url

import django_monitor

from .models import GroundtruthRecord
from .views import AddGroundtruthRecordView


urlpatterns = patterns('',

    url(r'^add/$', AddGroundtruthRecordView.as_view(),
        name='add_groundtruthrecord'),

)


django_monitor.nq(GroundtruthRecord)

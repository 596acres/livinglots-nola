from django.conf.urls import patterns, url

import livinglots_lots.urls as llurls

from .views import LotsCountViewWithAcres, LotsGeoJSONCentroid


urlpatterns = patterns('',

    url(r'^geojson-centroid/', LotsGeoJSONCentroid.as_view(),
        name='nola_lot_geojson_centroid'),
    url(r'^count/', LotsCountViewWithAcres.as_view(), name='lot_count'),

) + llurls.urlpatterns

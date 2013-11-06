from django.conf.urls import patterns, url

import livinglots_lots.urls as llurls

from .views import LotsGeoJSONCentroid


urlpatterns = patterns('',

    url(r'^geojson-centroid/', LotsGeoJSONCentroid.as_view(),
        name='nola_lot_geojson_centroid'),

) + llurls.urlpatterns

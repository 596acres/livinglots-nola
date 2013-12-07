from django.conf.urls import patterns, url

import livinglots_lots.urls as llurls

from .views import (LotsCountViewWithAcres, LotsGeoJSONCentroid,
                    LotsGeoJSONPolygon, LotsOwnershipOverview)


urlpatterns = patterns('',

    url(r'^geojson-centroid/', LotsGeoJSONCentroid.as_view(),
        name='nola_lot_geojson_centroid'),
    url(r'^geojson-polygon/', LotsGeoJSONPolygon.as_view(),
        name='lot_geojson_polygon'),
    url(r'^count/ownership/', LotsOwnershipOverview.as_view(),
        name='lot_ownership_overview'),
    url(r'^count/', LotsCountViewWithAcres.as_view(), name='lot_count'),

) + llurls.urlpatterns

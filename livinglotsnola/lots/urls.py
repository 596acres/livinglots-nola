from django.conf.urls import patterns, url

import livinglots_lots.urls as llurls

from .views import (LotsCountViewWithAcres, LotsGeoJSONCentroid,
                    LotsGeoJSONPolygon, LotsOwnershipOverview, NolaLotsCSV,
                    NolaLotsKML, NolaLotsGeoJSON)


urlpatterns = patterns('',

    url(r'^geojson-centroid/', LotsGeoJSONCentroid.as_view(),
        name='nola_lot_geojson_centroid'),
    url(r'^geojson-polygon/', LotsGeoJSONPolygon.as_view(),
        name='lot_geojson_polygon'),
    url(r'^count/ownership/', LotsOwnershipOverview.as_view(),
        name='lot_ownership_overview'),
    url(r'^count/', LotsCountViewWithAcres.as_view(), name='lot_count'),
    url(r'^csv/', NolaLotsCSV.as_view(), name='csv'),
    url(r'^kml/', NolaLotsKML.as_view(), name='kml'),
    url(r'^geojson/', NolaLotsGeoJSON.as_view(), name='geojson'),

) + llurls.urlpatterns

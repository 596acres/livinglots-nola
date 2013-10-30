import geojson
import json

from inplace.views import GeoJSONListView
from livinglots_lots.views import FilteredLotsMixin


class LotGeoJSONMixin(object):

    def get_feature(self, lot):
        if lot.known_use:
            layer = 'in use'
        elif lot.owner and lot.owner.owner_type == 'public':
            layer = 'public'
        elif lot.owner and lot.owner.owner_type == 'private':
            layer = 'private'
        else:
            layer = ''

        try:
            lot_geojson = lot.geojson
        except Exception:
            if lot.polygon:
                lot_geojson = lot.polygon.geojson
            else:
                lot_geojson = lot.centroid.geojson
        return geojson.Feature(
            lot.pk,
            geometry=json.loads(lot_geojson),
            properties={
                'address_line1': lot.address_line1,
                'layer': layer,
                'pk': lot.pk,
            },
        )


class LotsGeoJSONCentroid(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().qs.filter(centroid__isnull=False).geojson(
            field_name='centroid',
            precision=8,
        ).select_related('known_use', 'owner__owner_type')

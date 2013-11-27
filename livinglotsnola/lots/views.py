import geojson
import json
from pint import UnitRegistry

from django.db.models import Count, Sum

from inplace.views import GeoJSONListView
from livinglots_genericviews.views import JSONResponseView
from livinglots_lots.views import FilteredLotsMixin, LotsCountView


ureg = UnitRegistry()


class LotGeoJSONMixin(object):

    def get_acres(self, lot):
        acres = getattr(lot, 'area_acres', None)
        if not acres:
            return 'unknown'
        return round(acres, 2)

    def get_feature(self, lot):
        if lot.known_use:
            layer = 'in use'
        elif lot.owner and lot.owner.owner_type == 'public':
            layer = 'public'
        elif lot.owner and lot.owner.owner_type == 'private':
            layer = 'private'
            if lot.has_blight_liens:
                layer = 'private_blight_liens'
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
                'has_organizers': lot.organizers.count() > 0,
                'layer': layer,
                'owner': str(lot.owner) or 'unknown',
                'pk': lot.pk,
                'size': self.get_acres(lot),
            },
        )


class LotsGeoJSONCentroid(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().qs.filter(centroid__isnull=False).geojson(
            field_name='centroid',
            precision=8,
        ).select_related('known_use', 'owner__owner_type')


class LotsOwnershipOverview(FilteredLotsMixin, JSONResponseView):

    def get_owners(self, lots_qs):
        owners = []
        for row in lots_qs.values('owner__name').annotate(count=Count('pk')):
            owners.append({
                'name': row['owner__name'],
                'count': row['count'],
            })
        return owners

    def get_layers(self, lots):
        return {
            'private': lots.filter(
                owner__owner_type='private',
                has_blight_liens=False
            ),
            'public': lots.filter(owner__owner_type='public'),
        }

    def get_layer_counts(self, layers):
        for layer, qs in layers.items():
            yield {
                'type': layer,
                'owners': self.get_owners(qs),
            }

    def get_context_data(self, **kwargs):
        lots = self.get_lots().qs
        layers = self.get_layers(lots)
        return list(self.get_layer_counts(layers))


class LotsCountViewWithAcres(LotsCountView):

    def get_area_in_acres(self, lots_qs):
        sqft = lots_qs.aggregate(total_area=Sum('polygon_area'))['total_area']
        if not sqft:
            return 0
        sqft = sqft * (ureg.feet ** 2)
        acres = sqft.to(ureg.acre).magnitude
        return int(round(acres))

    def get_context_data(self, **kwargs):
        lots = self.get_lots().qs
        no_known_use = lots.filter(known_use__isnull=True)
        in_use = lots.filter(known_use__isnull=False, known_use__visible=True)

        context = {
            'lots-count': lots.count(),
            'lots-acres': self.get_area_in_acres(lots),
            'no-known-use-count': no_known_use.count(),
            'no-known-use-acres': self.get_area_in_acres(no_known_use),
            'in-use-count': in_use.count(),
            'in-use-acres': self.get_area_in_acres(in_use),
        }
        return context

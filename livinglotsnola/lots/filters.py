from django.db.models import Q

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D

import django_filters

from .models import Lot


class BoundingBoxFilter(django_filters.Filter):

    def filter(self, qs, value):
        bbox = Polygon.from_bbox(value.split(','))
        return qs.filter(centroid__within=bbox)


class LayerFilter(django_filters.Filter):

    def filter(self, qs, value):
        layers = value.split(',')
        layer_filter = Q()
        for layer in layers:
            if layer == 'public':
                layer_filter = layer_filter | Q(owner__owner_type='public')
            if layer == 'private':
                layer_filter = layer_filter | Q(owner__owner_type='private')
        return qs.filter(layer_filter)


class LotGroupParentFilter(django_filters.Filter):

    def filter(self, qs, value):
        if value == 'true':
            qs = qs.filter(group=None)
        return qs


class LotCenterFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        try:
            lot = Lot.objects.get(pk=value)
        except Exception:
            return qs
        return qs.filter(centroid__distance_lte=(lot.centroid, D(mi=.5)))


class OwnerFilter(django_filters.Filter):

    def __init__(self, owner_type=None, **kwargs):
        super(OwnerFilter, self).__init__(**kwargs)
        self.owner_type = owner_type

    def filter(self, qs, value):
        if not value:
            return qs
        owner_pks = value.split(',')
        owner_query = Q(
            owner__owner_type=self.owner_type,
            owner__pk__in=owner_pks,
        )
        other_owners_query = ~Q(owner__owner_type=self.owner_type)
        return qs.filter(owner_query | other_owners_query)


class LotFilter(django_filters.FilterSet):

    bbox = BoundingBoxFilter()
    layers = LayerFilter()
    lot_center = LotCenterFilter()
    parents_only = LotGroupParentFilter()
    public_owners = OwnerFilter(owner_type='public')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LotFilter, self).__init__(*args, **kwargs)
        # TODO adjust initial queryset based on user
        self.user = user

    class Meta:
        model = Lot
        fields = [
            'address_line1',
            'bbox',
            'known_use',
            'layers',
            'lot_center',
            'parents_only',
            'public_owners',
        ]

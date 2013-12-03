from django.db.models import Q

from django.contrib.gis.geos import Polygon

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


class LotFilter(django_filters.FilterSet):

    bbox = BoundingBoxFilter()
    layers = LayerFilter()

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
        ]

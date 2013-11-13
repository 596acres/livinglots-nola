from django.contrib.gis.geos import Polygon

import django_filters

from .models import Lot


class BoundingBoxFilter(django_filters.Filter):

    def filter(self, qs, value):
        bbox = Polygon.from_bbox(value.split(','))
        return qs.filter(centroid__within=bbox)


class LotFilter(django_filters.FilterSet):

    bbox = BoundingBoxFilter()

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
        ]

from hashlib import sha1

from django.db.models import Q

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D

import django_filters

from noladata.councildistricts.models import CouncilDistrict
from noladata.neighborhoodgroups.models import NeighborhoodGroup
from noladata.zipcodes.models import ZipCode

from .models import Lot


class BoundingBoxFilter(django_filters.Filter):

    def filter(self, qs, value):
        bbox = Polygon.from_bbox(value.split(','))
        return qs.filter(centroid__within=bbox)


class LayerFilter(django_filters.Filter):

    def filter(self, qs, value):
        layers = value.split(',')
        # If lot is a project, it doesn't matter what the owner is. Projects
        # filtered by ProjectFilter, so allow them all through here
        layer_filter = Q(known_use__visible=True, owner=None)

        for layer in layers:
            if layer == 'public':
                layer_filter = layer_filter | Q(
                    Q(known_use=None) | Q(known_use__visible=True),
                    owner__owner_type='public',
                )
            elif layer == 'private':
                layer_filter = layer_filter | Q(
                    Q(known_use=None) | Q(known_use__visible=True),
                    owner__owner_type='private',
                    has_blight_liens=False,
                )
            elif layer == 'private_blight_liens':
                layer_filter = layer_filter | Q(
                    Q(known_use=None) | Q(known_use__visible=True),
                    owner__owner_type='private',
                    has_blight_liens=True,
                )
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


class NeighborhoodGroupFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        boundary = NeighborhoodGroup.objects.get(label=value)
        return qs.filter(centroid__within=boundary.geometry)


class OwnerFilter(django_filters.Filter):

    def __init__(self, owner_type=None, **kwargs):
        super(OwnerFilter, self).__init__(**kwargs)
        self.owner_type = owner_type

    def filter(self, qs, value):
        if not value:
            return qs
        owner_pks = value.split(',')
        owner_query = Q(
            Q(known_use=None) | Q(known_use__visible=True),
            owner__owner_type=self.owner_type,
            owner__pk__in=owner_pks,
        )
        other_owners_query = ~Q(owner__owner_type=self.owner_type)
        return qs.filter(owner_query | other_owners_query)


class ZipCodeFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        zipcode = ZipCode.objects.get(label=value)
        return qs.filter(centroid__within=zipcode.geometry)


class CouncilDistrictFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        boundary = CouncilDistrict.objects.get(label=value)
        return qs.filter(centroid__within=boundary.geometry)


class ProjectFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value or value == 'include':
            return qs
        has_project_filter = Q(known_use__visible=True)
        if value == 'include':
            return qs
        elif value == 'exclude':
            return qs.filter(~has_project_filter)
        elif value == 'only':
            return qs.filter(has_project_filter)
        return qs


class LotFilter(django_filters.FilterSet):

    bbox = BoundingBoxFilter()
    council_district = CouncilDistrictFilter()
    layers = LayerFilter()
    lot_center = LotCenterFilter()
    neighborhood_group = NeighborhoodGroupFilter()
    parents_only = LotGroupParentFilter()
    projects = ProjectFilter()
    public_owners = OwnerFilter(owner_type='public')
    zipcode = ZipCodeFilter()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LotFilter, self).__init__(*args, **kwargs)
        # TODO adjust initial queryset based on user
        self.user = user

    def hashkey(self):
        return sha1(repr(sorted(self.data.items()))).hexdigest()

    class Meta:
        model = Lot
        fields = [
            'address_line1',
            'bbox',
            'council_district',
            'known_use',
            'layers',
            'lot_center',
            'neighborhood_group',
            'parents_only',
            'projects',
            'public_owners',
            'zipcode',
        ]

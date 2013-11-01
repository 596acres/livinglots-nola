from noladata.buildings.models import Building
from noladata.habitat.load import lots_available_for_gardening
from noladata.nora.models import UncommittedProperty
from noladata.parcels.models import Parcel

from owners.models import Owner
from .models import Lot


class NoraUncommittedPropertiesFinder(object):

    def get_owner(self):
        owner, created = Owner.objects.get_or_create('New Orleans Redevelopment Authority', defaults={
            'owner_type': 'public',
        })
        return owner

    def find_parcel(self, uncommitted_property):
        # Get Parcels using the uncommitted_property's address
        parcels = Parcel.objects.filter_by_address(
            uncommitted_property.property_address
        )
        if not parcels.count():
            print 'Could not find parcels for %s' % (
                uncommitted_property.property_address
            )

            # Look for Parcels using the uncommitted_property's point,
            # which is unreliable but worth a shot
            parcels = Parcel.objects.filter(
                geom__contains=uncommitted_property.geom
            )
            print 'Found parcel by point:', parcels

        for parcel in parcels:
            buildings = Building.objects.filter_by_parcel(parcel)
            if buildings.count():
                print ('Found a building on one of the parcels for '
                        '%s--skipping') % uncommitted_property.property_address
                continue
            else:
                print 'No building on parcel %d' % parcel.pk
                return parcel
        return None

    def find_lots(self):
        owner = self.get_owner()
        for uncommitted_property in UncommittedProperty.objects.all():
            parcel = self.find_parcel(uncommitted_property)
            if not parcel:
                continue
            lot = Lot(
                parcel=parcel,
                polygon=parcel.geom,
                centroid=parcel.geom.centroid,
                address_line1=uncommitted_property.property_address,
                city=uncommitted_property.city,
                state_province=uncommitted_property.state,
                country='USA',
                known_use_certainty=7,
                owner=owner,
            )
            lot.save()


class HabitatLotsAvailableForGardeningFinder(object):

    def find_parcel(self, lot_available):
        # Search by GEOPIN
        parcels = Parcel.objects.filter(geopin=lot_available['properties']['GEOPIN'])
        if not parcels.count():
            # Search by address
            filters = {}
            address_properties = ('SITUS_DIR', 'SITUS_STRE', 'SITUS_TYPE',
                                  'SITUS_NUMB',)
            for p in address_properties:
                if lot_available['properties'][p]:
                    filters[p.lower() + '__iexact'] = lot_available['properties'][p]
            parcels = Parcel.objects.filter(**filters)
        if parcels.count() > 1:
            print 'Found too many parcels for %s' % lot_available
            return None
        if parcels.count() == 0:
            print 'Found zero parcels for %s' % lot_available
            return None
        return parcels[0]

    def get_owner(self):
        owner, created = Owner.objects.get_or_create('Habitat for Humanity', defaults={
            'owner_type': 'private',
        })
        return owner

    def find_lots(self):
        owner = self.get_owner()
        for lot_available in lots_available_for_gardening():
            parcel = self.find_parcel(lot_available)
            if not parcel:
                continue
            lot = Lot(
                parcel=parcel,
                polygon=parcel.geom,
                centroid=parcel.geom.centroid,
                address_line1=parcel.address,
                city='New Orleans',
                state_province='LA',
                country='USA',
                known_use_certainty=7,
                owner=owner,
            )
            lot.save()

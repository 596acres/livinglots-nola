from noladata.buildings.models import Building
from noladata.nora.models import UncommittedProperty
from noladata.parcels.models import Parcel

from .models import Lot


class NoraUncommittedPropertiesFinder(object):

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
        for uncommitted_property in UncommittedProperty.objects.all():
            parcel = self.find_parcel(uncommitted_property)
            if not parcel:
                continue
            lot = Lot(
                polygon=parcel.geom,
                centroid=parcel.geom.centroid,
                address_line1=uncommitted_property.property_address,
                city=uncommitted_property.city,
                state_province=uncommitted_property.state,
                country='USA',
                known_use_certainty=7,
                # TODO set owner to HANO
            )
            lot.save()

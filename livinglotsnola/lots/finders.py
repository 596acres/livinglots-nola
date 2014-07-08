from django.contrib.gis.geos import Point

from livinglots_lots.load import get_addresses_in_range
from noladata.habitat.load import lots_available_for_gardening
from noladata.hano.models import ScatteredSite
from noladata.nora.models import UncommittedProperty
from noladata.parcels.models import Parcel

from livinglotsnola.geocode import nominatim
from owners.models import Owner
from .models import Lot, LotGroup


def find_existing_lot(parcel=None, address=None, geom=None):
    """
    Try to find existing lots, in order of least to most expensive. Returns
    as soon as any of the conditions filters the number of lots to 1.
    """
    lots = Lot.objects.all()
    if parcel:
        lots = lots.filter(parcel=parcel)
        if lots.count() == 1:
            return lots
    if address:
        lots = lots.filter(address_line1__iexact=address)
        if lots.count() == 1:
            return lots
    if geom:
        lots = lots.filter(polygon__overlaps=geom)
        if lots.count() == 1:
            return lots
    return lots


class HanoScatteredSitesFinder(object):

    def get_owner(self):
        owner, created = Owner.objects.get_or_create('Housing Authority of New Orleans', defaults={
            'owner_type': 'public',
        })
        return owner

    def find_parcel(self, address):
        parcels = Parcel.objects.filter_by_address_fuzzy(address)
        if parcels.count():
            return parcels[0]
        if not parcels:
            geocoded = nominatim(street=address, city='New Orleans',
                                 state='Louisiana')
            geocoded_point = Point(geocoded['lon'], geocoded['lat'])
            parcels = Parcel.objects.filter(geom__contains=geocoded_point)
            if parcels.count():
                return parcels[0]
        return None

    def find_lots(self):
        owner = self.get_owner()
        default_kwargs = {
            'city': 'New Orleans',
            'state_province': 'LA',
            'country': 'USA',
            'known_use_certainty': 7,
            'owner': owner,
        }
        for site in ScatteredSite.objects.filter(lot=None):
            site_lots = set()
            default_kwargs['name'] = site.address
            for address in get_addresses_in_range(site.address):
                parcel = self.find_parcel(address)

                if not parcel:
                    print ('Could not find parcel for address "%s" within '
                           'scattered site "%s"') % (address, site.address)
                    continue

                # If already added as a lot, update the lot and move on
                existing_lots = find_existing_lot(parcel=parcel,
                                                  address=address)
                if existing_lots:
                    for lot in existing_lots:
                        lot.scattered_sites.add(site)
                        lot.save()
                        site_lots.add(lot)
                    continue

                # Save lot
                lot = Lot(
                    parcel=parcel,
                    polygon=parcel.geom,
                    centroid=parcel.geom.centroid,
                    address_line1=address,
                    added_reason="in HANO's scattered sites list",
                    **default_kwargs
                )
                lot.save()
                site_lots.add(lot)

            # Add to lot group if there are multiple lots for this site
            if len(site_lots) > 1:
                lot_group = LotGroup(
                    address_line1=site.address,
                    **default_kwargs
                )
                lot_group.save()

                for lot in site_lots:
                    lot_group.add(lot)


class NoraUncommittedPropertiesFinder(object):

    # TODO clean this up a bit, make it possible / quick to find lots added
    #  dynamically using a Synchronizer

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
            if not parcel.probably_is_vacant:
                print '%s is probably not vacant--skipping' % (
                    uncommitted_property.property_address,
                )
                continue
            else:
                print 'Parcel %d is probably vacant' % parcel.pk
                return parcel
        return None

    def hide_old_lots(self):
        """Hide lots with UncommittedProperty that is not current."""
        for old_property in UncommittedProperty.objects.filter(status='old'):
            old_property.lot_set.update(owner=None)

    def find_lots(self):
        owner = self.get_owner()
        for uncommitted_property in UncommittedProperty.objects.filter(status='current'):
            # This property might already have a lot. If so, move along.
            if uncommitted_property.lot_set.exists():
                continue

            # Get parcel
            parcel = self.find_parcel(uncommitted_property)
            if not parcel:
                continue

            # Get existing lots
            existing_lots = find_existing_lot(
                parcel=parcel,
                address=uncommitted_property.property_address,
                geom=parcel.geom,
            )
            if existing_lots:
                if existing_lots.count() == 1:
                    # Save uncommitted_property to lot
                    existing_lot = existing_lots[0]
                    existing_lot.uncommitted_properties.add(uncommitted_property)
                    existing_lot.save()
                print 'Lot already exists. Skipping.'
                continue

            # Save lot
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
                added_reason="in NORA's uncommitted properties list",
            )
            lot.save()
            lot.uncommitted_properties.add(uncommitted_property)


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
                added_reason="in Habitat for Humanity's potential gardens list",
            )
            lot.save()


class PrivateLotsWithBlightLiensFinder(object):

    def find_lots(self):
        # Generic private owner
        owner, created = Owner.objects.get_or_create('private owner', defaults={
            'owner_type': 'private',
        })

        kwargs = {
            'city': 'New Orleans',
            'state_province': 'LA',
            'country': 'USA',
            'known_use_certainty': 7,
            'owner': owner,
            'added_reason': "has blight liens",
            'has_blight_liens': True,
        }

        for parcel in Parcel.objects.exclude(lien=None).filter(lot=None):
            if not parcel.probably_is_vacant():
                continue
            try:
                lot = Lot(
                    parcel=parcel,
                    polygon=parcel.geom,
                    centroid=parcel.geom.centroid,
                    address_line1=parcel.address,
                    **kwargs
                )
                lot.save()
            except Exception:
                import traceback
                traceback.print_exc()
                continue

from time import sleep

from django.utils.timezone import now

from noladata.assessor.load import load_tax_bill_number
from noladata.buildings.models import Building
from noladata.codeenforcement.models import Case
from noladata.habitat.load import lots_available_for_gardening
from noladata.nora.models import UncommittedProperty
from noladata.parcels.models import Parcel
from noladata.treasury.load import load_code_lien_information

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
            if not parcel.probably_is_vacant:
                print '%s is probably not vacant--skipping' % (
                    uncommitted_property.property_address,
                )
                continue
            else:
                print 'Parcel %d is probably vacant' % parcel.pk
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
                added_reason="in NORA's uncommitted properties list",
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
                added_reason="in Habitat for Humanity's potential gardens list",
            )
            lot.save()


class PrivateLotsWithBlightLiensFinder(object):

    def find_parcel(self, case):
        # Search by GEOPIN
        parcels = Parcel.objects.filter(geopin=case.geopin)
        if not parcels.count():
            # TODO Search by location and/or geom
            return None
        return parcels[0]

    def get_blight_liens(self, parcel):
        tax_bill_number = load_tax_bill_number(parcel.situs_numb,
                                               parcel.situs_stre,
                                               parcel.situs_type,
                                               street_direction=parcel.situs_dir)
        if not tax_bill_number:
            raise Exception('Could not find tax bill number for Parcel %d' %
                            parcel.pk)
        return list(load_code_lien_information(tax_bill_number))

    def find_lots(self):
        # Generic private owner
        owner, created = Owner.objects.get_or_create('private owner', defaults={
            'owner_type': 'private',
        })

        for case in Case.objects.all():
            try:
                parcel = self.find_parcel(case)
                if not parcel:
                    print 'No parcel found for %s' % case.location
                    continue

                # Check whether there is a building on the property
                if Building.objects.filter_by_parcel(parcel).count():
                    print ('*** Parcel contains a building. Probably should '
                           'not add')

                # Wait a bit between requests
                sleep(.1)

                # Try to find liens on this property
                liens = self.get_blight_liens(parcel)
                if not liens:
                    print 'No blight liens found for %s' % case.location
                    continue
                else:
                    print 'Found blight liens for %s. Adding.' % case.location
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
                    added_reason="in Code Enforcement Active Pipeline",
                    has_blight_liens=True,
                    blight_liens_last_checked=now(),
                )
                lot.save()
            except Exception:
                import traceback
                traceback.print_exc()
                continue

from pint import UnitRegistry

from django.contrib.contenttypes import generic
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from noladata.zipcodes.models import ZipCode

from livinglots_lots.models import BaseLot, BaseLotGroup, BaseLotManager
from livinglots_lots.signals import lot_details_loaded

from organize.models import Organizer
from .exceptions import ParcelAlreadyInLot


ureg = UnitRegistry()


class LotManager(BaseLotManager):

    def create_lot_for_parcels(self, parcels, **lot_kwargs):
        lots = []

        # Check parcel validity
        for parcel in parcels:
            if parcel.lot_set.count():
                raise ParcelAlreadyInLot()

        # Create lots for each parcel
        for parcel in parcels:
            kwargs = {
                'parcel': parcel,
                'polygon': parcel.geom,
                'centroid': parcel.geom.centroid,
                'address_line1': parcel.address,
                'name': parcel.address,
            }
            kwargs.update(**lot_kwargs)
            lot = Lot(**kwargs)
            lot.save()
            lots.append(lot)

        # Multiple lots, create a lot group
        if len(lots) > 1:
            example_lot = lots[0]
            kwargs = {
                'address_line1': example_lot.address_line1,
                'name': example_lot.name,
            }
            kwargs.update(**lot_kwargs)
            lot = LotGroup(**kwargs)
            lot.save()
            lot.update(lots=lots)
        return lot


class LotGroupLotMixin(models.Model):

    group = models.ForeignKey('LotGroup',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('group'),
    )

    class Meta:
        abstract = True


class LotMixin(models.Model):

    parcel = models.ForeignKey('parcels.Parcel',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    organizers = generic.GenericRelation(Organizer)

    uncommitted_properties = models.ManyToManyField('nora.UncommittedProperty',
        null=True,
        blank=True
    )

    scattered_sites = models.ManyToManyField('hano.ScatteredSite',
        null=True,
        blank=True
    )

    has_blight_liens = models.BooleanField(_('has blight liens'),
        default=False,
    )

    @classmethod
    def get_filter(cls):
        from .filters import LotFilter
        return LotFilter

    def calculate_polygon_area(self):
        try:
            return self.polygon.transform(3452, clone=True).area
        except Exception:
            return None

    def _area(self):
        if not self.polygon_area:
            self.polygon_area = self.calculate_polygon_area()
            self.save()
        return self.polygon_area

    area = property(_area)

    def _area_acres(self):
        area = self.area * (ureg.feet ** 2)
        return area.to(ureg.acre).magnitude

    area_acres = property(_area_acres)

    def _in_scattered_sites(self):
        # Trivial case--lot itself has associated ScatteredSite instances
        if self.scattered_sites.count():
            return True

        # Else, if we have a group, look at its lots for ScatteredSites
        if self.lotgroup:
            if self.lotgroup.lot_set.exclude(scattered_sites=None).count():
                return True
        return False

    in_scattered_sites = property(_in_scattered_sites)

    def _in_uncommitted_properties(self):
        # Trivial case--lot itself has associated ScatteredSite instances
        if self.uncommitted_properties.count():
            return True

        # Else, if we have a group, look at its lots for ScatteredSites
        if self.lotgroup:
            if self.lotgroup.lot_set.exclude(uncommitted_properties=None).count():
                return True
        return False

    in_uncommitted_properties = property(_in_uncommitted_properties)

    def _postal_code(self):
        try:
            return ZipCode.objects.get(geometry__contains=self.centroid)
        except ZipCode.DoesNotExist:
            return None

    class Meta:
        abstract = True


class Lot(LotMixin, LotGroupLotMixin, BaseLot):

    objects = LotManager()

    class Meta:
        permissions = (
            ('view_preview', 'Can view preview map'),
        )


class LotGroup(BaseLotGroup, Lot):
    objects = models.Manager()


@receiver(lot_details_loaded)
def load_lazy_properties(sender, instance=None, **kwargs):
    # TODO also things like ParcelAssessorRecord
    if not instance.postal_code:
        instance.postal_code = instance._postal_code().label
        instance.save()

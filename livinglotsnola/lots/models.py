from pint import UnitRegistry

from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _

from livinglots_lots.models import BaseLot, BaseLotGroup

from organize.models import Organizer


ureg = UnitRegistry()


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

    blight_liens_last_checked = models.DateTimeField(
        _('blight liens last checked'),
        blank=True,
        null=True,
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

    class Meta:
        abstract = True


class Lot(LotMixin, LotGroupLotMixin, BaseLot):

    class Meta:
        permissions = (
            ('view_preview', 'Can view preview map'),
        )


class LotGroup(LotGroupLotMixin, BaseLotGroup):
    pass

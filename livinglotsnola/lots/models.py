from django.db import models
from django.utils.translation import ugettext_lazy as _

from livinglots_lots.models import BaseLot, BaseLotGroup


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

    class Meta:
        abstract = True


class Lot(LotMixin, LotGroupLotMixin, BaseLot):
    pass


class LotGroup(LotGroupLotMixin, BaseLotGroup):
    pass

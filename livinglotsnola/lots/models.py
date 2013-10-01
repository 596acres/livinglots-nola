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


class Lot(LotGroupLotMixin, BaseLot):
    pass


class LotGroup(LotGroupLotMixin, BaseLotGroup):
    pass

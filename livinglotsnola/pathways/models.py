from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from caching.base import CachingQuerySet, CachingMixin
from feincms.models import Base

from livinglots_pathways.cms import PathwayFeinCMSMixin
from livinglots_pathways.models import BasePathway, BasePathwayManager


class PathwayManager(BasePathwayManager):

    def get_queryset(self):
        return CachingQuerySet(self.model, self._db)

    def get_for_lot(self, lot):
        qs = super(PathwayManager, self).get_for_lot(lot)
        if lot.has_blight_liens:
            qs.filter(
                Q(has_blight_liens__isnull=True) |
                Q(has_blight_liens=True)
            )
        else:
            qs.filter(
                Q(has_blight_liens__isnull=True) |
                Q(has_blight_liens=False)
            )
        return qs


class Pathway(CachingMixin, PathwayFeinCMSMixin, BasePathway, Base):
    objects = PathwayManager()

    has_blight_liens = models.NullBooleanField(_('has blight liens'),
        help_text = _('If true, this pathway applies to lots with blight '
                      'liens. If false, it applies to lots without blight '
                      'liens. If not set, it applies to lots with or without '
                      'blight liens.')
    )

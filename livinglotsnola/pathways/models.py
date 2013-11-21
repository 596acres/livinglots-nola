from feincms.models import Base

from livinglots_pathways.cms import PathwayFeinCMSMixin
from livinglots_pathways.models import BasePathway


class Pathway(PathwayFeinCMSMixin, BasePathway, Base):
    pass

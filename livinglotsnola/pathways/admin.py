from django.contrib import admin

from livinglots_pathways.admin import BasePathwayAdmin

from .models import Pathway


class PathwayAdmin(BasePathwayAdmin):
    pass


admin.site.register(Pathway, PathwayAdmin)

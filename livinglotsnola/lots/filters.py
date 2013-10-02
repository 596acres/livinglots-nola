import django_filters

from .models import Lot


class LotFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LotFilter, self).__init__(*args, **kwargs)
        # TODO adjust initial queryset based on user
        self.user = user

    class Meta:
        model = Lot
        fields = ['address_line1', 'known_use',]

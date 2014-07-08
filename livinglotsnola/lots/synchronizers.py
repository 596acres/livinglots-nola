from external_data_sync import register, synchronizers

from .finders import (NoraUncommittedPropertiesFinder,
                      PrivateLotsWithBlightLiensFinder)


class LotsWithLiensSynchronizer(synchronizers.Synchronizer):

    def sync(self, data_source):
        finder = PrivateLotsWithBlightLiensFinder()
        finder.find_lots()


class LotsWithUncommittedPropertySynchronizer(synchronizers.Synchronizer):

    def sync(self, data_source):
        finder = NoraUncommittedPropertiesFinder()
        finder.hide_old_lots()
        finder.find_lots()


register(LotsWithLiensSynchronizer)
register(LotsWithUncommittedPropertySynchronizer)

from external_data_sync import register, synchronizers

from .finders import PrivateLotsWithBlightLiensFinder


class LotsWithLiensSynchronizer(synchronizers.Synchronizer):

    def sync(self, data_source):
        finder = PrivateLotsWithBlightLiensFinder()
        finder.find_lots()


register(LotsWithLiensSynchronizer)

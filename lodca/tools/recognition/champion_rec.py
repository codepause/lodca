from epta.core import *


class EasyChampionRecognition(BaseTool):
    def __init__(self, *args, **kwargs):
        super(EasyChampionRecognition, self).__init__(*args, **kwargs)

    @staticmethod
    def use(self, *args, **kwargs):
        return None


class ConfigChampionRecognition(BaseTool, ConfigDependent):
    def __init__(self, *args, **kwargs):
        super(ConfigChampionRecognition, self).__init__(*args, **kwargs)

    def use(self, *args, **kwargs) -> dict:
        return {'name': self.config.settings.champion}

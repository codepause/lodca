from lodca.database.base_stats import BaseStatsDatabase
from lodca.database.item import ItemDatabase
from lodca.database.champion import ChampionDatabase

class DataBase:
    def __init__(self):
        self.base_stats = BaseStatsDatabase()
        self.items = ItemDatabase()
        self.champions = ChampionDatabase()

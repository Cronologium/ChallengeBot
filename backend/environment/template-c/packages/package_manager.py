class PackageManager:
    def fetch(self, id):
        if id == 1:
            from api.g001_battleships_api import BattleshipsApi
            from client.g001_battleships_client import BattleshipsClient
            return BattleshipsApi, BattleshipsClient
        if id == 2:
            from api.g002_xando_api import XandoApi
            from client.g002_xando_client import XandoClient
            return XandoApi, XandoClient
        else:
            raise NotImplementedError
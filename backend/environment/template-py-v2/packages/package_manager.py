class PackageManager:
    def fetch(self, id):
        if id == 1:
            from api.battleships_api import BattleshipsApi
            from client.battleships_client import BattleshipsClient
            return BattleshipsApi, BattleshipsClient
        else:
            raise NotImplementedError
import csv

class PlayerData:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.players_data = self._load_data()

    def _load_data(self):
        players_data = {}
        with open(self.csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                player_id = row['play_id']
                players_data[player_id] = {
                    'title': row['title'],
                    'ExitVelocity': row['ExitVelocity'],
                    'HitDistance': row['HitDistance'],
                    'LaunchAngle': row['LaunchAngle'],
                    'video': row['video']
                }
        return players_data

    def get_player_data(self, player_id):
        return self.players_data.get(player_id, None)

    def get_all_players(self):
        return self.players_data

# Example 
player_service = PlayerData('/workspaces/google-cloud-mlb/backend/datasets/2024-mlb-homeruns.csv')
player_data = player_service.get_player_data('148e943b-10db-4d71-943d-ead3b36bebbc')
print(player_data)

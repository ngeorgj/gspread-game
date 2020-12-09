from pprint import pprint

from game.server import Server
# INSTANCES
dinasty = Server()
game_data = dinasty.get_game_data()['data']
races = game_data['races']

# HELPER
def get_player_info(playername):
    response = dinasty.get_response()['Dinasty']['response']
    return response[playername][playername]


# ANSWER GROUPS

from pprint import pprint

from game.server import Server

dinasty = Server()
game_data = dinasty.get_game_data()['data']
races = game_data['races']

def get_player_info(playername):
    response = dinasty.get_response()['Dinasty']['response']
    return response[playername][playername]

EXTINCT = 'Extinct'
PLAYING = 'Playing'

P1 = 'P1'
P2 = 'P2'
P3 = 'P3'
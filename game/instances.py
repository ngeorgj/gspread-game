import os
import time
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

def press_key_to_continue():
    return input("\nPress 'any' Key to Continue!\n")

def sleep(seconds):
    return time.sleep(seconds)

def clear():
    return os.system('cls')

def debug(varname, content):
    print(f'[DEBUG {varname}] {content}')

def please_select_a_valid_option():
    print(" # Please Select a Valid Option.")

# ANSWER GROUPS

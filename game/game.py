import time
from pprint import pprint

from .instances import dinasty, game_data, press_key_to_continue
from .hardcoded_variables import EXTINCT, P1, P2, P3
from .player import Player


class Game:
    main_server_name = "Dinasty"

    keymapping = {
        'player1': {
            'nickname': 'C5',
            'title': 'C6',
            'race': 'C7',
            'population': 'C10',
            'minerals': 'C11',
            'gas': 'C12',
            'mining_ships': 'C15',
            'gas_ships': 'C16',
            'attack_ships': 'C17'
        },
        'player2': {
            'nickname': 'F5',
            'title': 'F6',
            'race': 'F7',
            'population': 'F10',
            'minerals': 'F11',
            'gas': 'F12',
            'mining_ships': 'F15',
            'gas_ships': 'F16',
            'attack_ships': 'F17'
        },
        'player3': {
            'nickname': 'I5',
            'title': 'I6',
            'race': 'I7',
            'population': 'I10',
            'minerals': 'I11',
            'gas': 'I12',
            'mining_ships': 'I15',
            'gas_ships': 'I16',
            'attack_ships': 'I17'
        }
    }

    positions = {
        'P1': 'player1',
        'P2': 'player2',
        'P3': 'player3'
    }

    def __init__(self):
        self.server = dinasty
        self.player = self.enter_game()
        self.play()

    def enter_game(self):
        # Create player instance
        player = Player()

        slots = dinasty.response['Dinasty']['slots']
        slots = [slot[0] for slot in slots.items() if slot[1] != 'Unavailable']

        if len(slots) == 0:
            print('No room for new players! \n \n')
            press_key_to_continue()
            quit()

        answer = self._alocate_player(slots)
        slot = self.positions[answer]

        if answer in slots:
            player.position = answer
            dinasty.open_sheet(dinasty.game_name, dinasty.server_name)

            # From Player Information
            dinasty.write_cell(self.keymapping[slot]['nickname'], player.name)
            dinasty.write_cell(self.keymapping[slot]['title'], player.title)
            dinasty.write_cell(self.keymapping[slot]['race'], player.race)

            # From Starting Values
            dinasty.write_cell(self.keymapping[slot]['population'],
                               game_data['races'][player.race]['sv']['population'])

            dinasty.write_cell(self.keymapping[slot]['minerals'],
                               game_data['races'][player.race]['sv']['minerals'])

            dinasty.write_cell(self.keymapping[slot]['gas'],
                               game_data['races'][player.race]['sv']['gas'])

            dinasty.write_cell(self.keymapping[slot]['mining_ships'],
                               game_data['races'][player.race]['sv']['mining_ships'])

            dinasty.write_cell(self.keymapping[slot]['gas_ships'],
                               game_data['races'][player.race]['sv']['gas_ships'])

            dinasty.write_cell(self.keymapping[slot]['attack_ships'],
                               game_data['races'][player.race]['sv']['attack_ships'])

        time.sleep(6)
        dinasty.get_response()

        return player

    def play(self):
        game_on = True
        while game_on:
            self.player.options()

            if self.player.my_info()['population'] <= 0:
                print('Your population is exticted!.')
                quit()

        self.server.clean()

    def _alocate_player(self, slots):
        """ This function will only be used if there are slots in the game room."""
        if P1 in slots:
            return P1
        elif P2 in slots:
            return P2
        elif P3 in slots:
            return P3


import time
from pprint import pprint

from .instances import dinasty, game_data
from .hardcoded_variables import EXTINCT
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
            'm_ships': 'C15',
            'g_ships': 'C16',
            'atk_ships': 'C17'
        },
        'player2': {
            'nickname': 'F5',
            'title': 'F6',
            'race': 'F7',
            'population': 'F10',
            'minerals': 'F11',
            'gas': 'F12',
            'm_ships': 'F15',
            'g_ships': 'F16',
            'atk_ships': 'F17'
        },
        'player3': {
            'nickname': 'I5',
            'title': 'I6',
            'race': 'I7',
            'population': 'I10',
            'minerals': 'I11',
            'gas': 'I12',
            'm_ships': 'I15',
            'g_ships': 'I16',
            'atk_ships': 'I17'
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
            input("Press 'any' key to close the game. \n")
            quit()

        answer = self._get_slots(slots)
        slot = self.positions[answer]

        if answer in slots:
            player.position = answer
            dinasty.open_sheet(dinasty.game_name, dinasty.server_name)

            # From Player Information
            dinasty.write_cell(self.keymapping[slot]['nickname'], player.name)
            dinasty.write_cell(self.keymapping[slot]['title'], player.title)
            dinasty.write_cell(self.keymapping[slot]['race'], player.race)

            # From Starting Values
            dinasty.write_cell(self.keymapping[slot]['population'], game_data['races'][player.race]['sv']['population'])
            dinasty.write_cell(self.keymapping[slot]['minerals'], game_data['races'][player.race]['sv']['minerals'])
            dinasty.write_cell(self.keymapping[slot]['gas'], game_data['races'][player.race]['sv']['gas'])
            dinasty.write_cell(self.keymapping[slot]['m_ships'], game_data['races'][player.race]['sv']['m_ships'])
            dinasty.write_cell(self.keymapping[slot]['g_ships'], game_data['races'][player.race]['sv']['g_ships'])
            dinasty.write_cell(self.keymapping[slot]['atk_ships'], game_data['races'][player.race]['sv']['atk_ships'])

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

    def _get_slots(self, slots):
        print(slots)
        print("Choose a Slot Below:")
        for slot in slots:
            print(" > ", slot)
        print()
        answer = input(" > ").upper()
        if answer not in self.positions:
            print("Please supply a valid answer!")
            answer = input(" > ")
            if answer in slots:
                return answer
        else:
            return answer

    def clean_check(self):
        players_data = dinasty.response[self.main_server_name]['response']

        statuses = []
        players_and_status = {}

        for player in players_data:
            status = players_data[player][player]['status']
            players_and_status[player] = status
            statuses.append(status)

        endgame_counter = 0
        for status in statuses:
            if status == EXTINCT:
                endgame_counter += 1

        if endgame_counter == 2:
            print("[LOG] Game Tables are being Wiped out.")
            dinasty.clean()

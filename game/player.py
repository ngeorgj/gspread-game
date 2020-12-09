import os

from .gsheet import GSheet
from .hangar import Hangar
from .instances import races, dinasty, game_data, get_player_info, clear, sleep, debug, please_select_a_valid_option

from .hardcoded_variables import (
    P1, P2, P3, ATTACK_GROUP,
    EXTRACT_GROUP, REFRESH_GROUP,
    MINE_GROUP, HANGAR_GROUP
)


class Player(Hangar):
    myturn = False

    position = ""
    enemies = []
    actions = 3

    def __init__(self):

        self.server = dinasty
        self.name = input("What is your name? \n -> ")
        self.nickname = input("What is your nickname? \n -> ")
        self.race = self.select_race()
        self.title = input("What is your title, Sr? \n -> ")

        self.prices = self.get_json(self.api_game_name,
                                    self.api_location,
                                    self.api_cell)['data']['ship_prices'][self.race]

        self.log = {'messages': [],
                    'battle': [],
                    'gathering': [],
                    'damage_taken': []}

    def attack(self):
        players = {}

        playing = list(dinasty.response['Dinasty']['response'].keys())

        pcounter = 1
        for player in playing:
            players[f'P{pcounter}'] = player

            pcounter += 1

        print("You can attack the following players:\n\n")
        for player in players.values():
            if player != self.name:
                print(" > ", player)

        def attack_recursion():
            print("What is your choice?")
            answer = input(" > ")
            if answer not in players.values():
                please_select_a_valid_option()
                attack_recursion()

            else:
                position = ''
                target = ''
                for player in players.items():
                    if player[1] == answer:
                        position = player[0]
                        target = player[1]

                return target, position

        target, target_position = attack_recursion()

        enemy_data = get_player_info(target)

        ships = int(self.attack_ships)
        ships_damage = int(game_data['races'][self.race]['sv']['atk_ships_dmg'])

        self.overwrite_property(target_position, 'population', int(enemy_data['population']) - (ships * ships_damage))
        self.actions -= 1
        self._check_actions()
        self.server.clean_check()

    def mine(self):
        ships = int(self.mining_ships)

        power = int(game_data['races'][self.race]['sv']['mining_ships_gathering_power'])
        my_minerals = int(self.my_info()['minerals'])
        self.overwrite_property(self.position, 'minerals', my_minerals + (ships * power))
        print(f"[LOG] {ships * power} Minerals were mined!")

        self.actions -= 1
        self._check_actions()

    def extract_gas(self):
        ships = int(self.gas_ships)
        power = int(game_data['races'][self.race]['sv']['gas_ships_gathering_power'])

        my_gas = self.my_info()['gas']

        self.overwrite_property(self.position, 'gas', int(my_gas) + (ships * power))
        print(f"[LOG] Extracted {ships * power} Gás!")

        self.actions -= 1
        self._check_actions()

    def options(self):
        os.system('cls')
        while not self.myturn:
            self.check_is_my_turn()
            print(f"# ==( WAIT FOR YOUR TURN )==============================\n")
            sleep(5)
            clear()
        actions = {
            'attack': self.attack,
            'mine': self.mine,
            'extract_gas': self.extract_gas,
            'hangar': self.ship_market
        }
        self.my_interface()
        for action in actions.items():
            print("  -> ", action[0])
        print(f" \n# ==( MARSHAL SAYS )==============================\n")
        print(f"      What will you do, sir?")
        print(f" \n# ==(  TYPE BELOW  )==============================")
        answer = str(input(" I will ")).lower()

        if answer in MINE_GROUP:
            clear()
            self.mine()

        elif answer in EXTRACT_GROUP:
            clear()
            self.extract_gas()

        elif answer in ATTACK_GROUP:
            clear()
            self.attack()

        elif answer in HANGAR_GROUP:
            clear()
            self.ship_market()

        self.options()

    def check_is_my_turn(self):
        self.open_sheet(self.api_game_name, 'SERVER')
        turn = self.read_cell(self.dinasty_turn_cell)
        if turn == self.position:
            self.myturn = True
            return True
        return False

    def select_race(self):  # Recursion
        print('You can choose a race from the list below:')
        for race in races.items():
            print(" > ", race[0])
        print()
        race = input('My Race: \n -> ').title()
        if race not in races.keys():
            please_select_a_valid_option()
            self.select_race()
        return race

    def pass_turn(self):
        self.actions = 3
        self.myturn = False
        if self.position == P1:
            self.change_turn_field(P2)
        elif self.position == P2:
            self.change_turn_field(P3)
        elif self.position == P3:
            self.change_turn_field(P1)

    def _check_actions(self):
        print(f"You have {self.actions} actions left!")
        if self.actions == 0:
            self.pass_turn()
        else:
            self.options()

    def my_info(self):
        return get_player_info(self.name)

    def my_interface(self):
        myinfo = self.my_info()
        print(f" # ================================================\n")
        print(f" #    Command Center of {self.name}, {self.title} \n")
        print(f" # ==( YOUR ECONOMY )===================================\n")
        print(f" # [ POPULATION ]        P {myinfo['population']}")
        print(f" # [  MINERALS  ]        M {myinfo['minerals']}")
        print(f" # [    GAS     ]        G {myinfo['gas']}\n")
        print(f" # ==(  YOUR SHIPS  )=====================================\n")
        print(f" # [ ATTACK SHIPS    ]   A {myinfo['attack_ships']}")
        print(f" # [ MINING SHIPS    ]   A {myinfo['attack_ships']}")
        print(f" # [ EXTRACTOR SHIPS ]   A {myinfo['attack_ships']}\n")
        print(f" # ==( YOUR ACTIONS )==============================\n")

    @property
    def mining_ships(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['mining_ships'])

    @property
    def gas_ships(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['gas_ships'])

    @property
    def attack_ships(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['attack_ships'])

    @property
    def population(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['population'])

    @property
    def minerals(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['minerals'])

    @property
    def gas(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['gas'])

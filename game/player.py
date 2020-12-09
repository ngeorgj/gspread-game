from .gsheet import GSheet
from .instances import races, dinasty, game_data, get_player_info, P1, P2, P3


class Player(GSheet):
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
                attack_recursion()

            else:
                position = ''
                for player in players.items():
                    if player[1] == answer:
                        position = player[0]

                return answer, position

        target, target_position = attack_recursion()

        enemy_data = get_player_info(target)

        ships = int(self.attack_ships)
        ships_damage = int(game_data['races'][self.race]['sv']['atk_ships_dmg'])

        self.overwrite_property(target_position, 'population', int(enemy_data['population']) - (ships * ships_damage))
        print("Worked!!")
        self.actions -= 1
        self._check_actions()

    def mine(self):
        ships = int(self.mining_ships)
        print(game_data['races'][self.race])
        power = int(game_data['races'][self.race]['sv']['m_ships_gath'])

        my_minerals = int(self.my_info()['minerals'])
        self.overwrite_property(self.position, 'minerals', my_minerals + (ships * power))
        print(f"[LOG] {ships * power} Minerals were mined!")

        self.actions -= 1
        self._check_actions()

    def extract_gas(self):
        ships = int(self.gas_ships)
        power = int(game_data['races'][self.race]['sv']['g_ships_gath'])

        my_gas = self.my_info()['gas']

        self.overwrite_property(self.position, 'gas', int(my_gas) + (ships * power))
        print(f"[LOG] Extracted {ships * power} Gás!")

        self.actions -= 1
        self._check_actions()

    def options(self):
        actions = {
            'attack': self.attack,
            'mine': self.mine,
            'extract_gas': self.extract_gas,
            'refresh': self.check_is_my_turn
        }
        print(f"\nMr. {self.name}, your possible actions are:\n")
        for action in actions.items():
            print(" > ", action[0])
        print("\nWhat will you do?\n")

        answer = str(input(" > ")).lower()

        if answer == 'mine':
            self.mine()
        elif answer in ['extract_gas', 'get gas', 'extract']:
            self.extract_gas()
        elif answer in ['ref', 'refresh', 'is my turn?']:
            if self.check_is_my_turn():
                self.options()
            else:
                print("Not your turn yet!")
                self.options()
        elif answer in ['attack', 'atk', 'deboxar', 'atacar']:
            self.attack()

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
        race = input('Your Race > ').title()
        if race not in races.keys():
            print("Please select a valid option.")
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

    @property
    def mining_ships(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['m_ships'])

    @property
    def gas_ships(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['g_ships'])

    @property
    def attack_ships(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['atk_ships'])

    @property
    def population(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['population'])

    @property
    def minerals(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['atk_ships'])

    @property
    def gas(self):
        self.open_sheet(self.api_game_name, self.server.server_name)
        return self.read_cell(self.PLAYERS_KEYMAP[self.position]['atk_ships'])

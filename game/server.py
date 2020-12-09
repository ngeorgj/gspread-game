import time

from game.gsheet import GSheet


class Server(GSheet):
    game_name = 'SpaceCraft'
    server_list = ['Dinasty']

    cell_dinasty = "J6"

    server_name = server_list[0]

    data = []
    players = []
    response = []

    is_running = False

    def __init__(self):
        self.get_response()

    def start_game(self, players: list):
        self.setup()
        self.is_running = True
        for player in players:
            self.players.append(player)

        self.welcome()

    def setup(self):
        self.data = self.get_json(self.game_name, self.api_tab_name, self.api_cell)

    def welcome(self):
        for player in self.players:
            player.log['messages'].append(f'Welcome {player.name}!')

    def get_response(self, supressed=True):
        data = self.get_json(self.game_name, self.api_location, self.cell_dinasty)
        self.response = data
        if not supressed:
            print("[LOG] Getting Response from Server...")
        time.sleep(2)
        return data

    def clean(self):
        self.open_sheet(self.game_name, "Dinasty")

        print("Wiping data out, tables are cristal clean!")

        cells_player1 = ['C5', 'C6', 'C7', 'C10', 'C11', 'C12', 'C15', 'C16', 'C17']
        cells_player2 = ['F5', 'F6', 'F7', 'F10', 'F11', 'F12', 'F15', 'F16', 'F17']
        cells_player3 = ['I5', 'I6', 'I7', 'I10', 'I11', 'I12', 'I15', 'I16', 'I17']

        cells_to_overwrite = [cells_player1, cells_player2, cells_player3]

        for group_of_cells in cells_to_overwrite:
            for cell in group_of_cells:
                self.write_cell(cell, "")

        self.change_turn_field('P1')
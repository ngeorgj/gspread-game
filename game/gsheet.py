import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GSheet:
    """
    Google SpreadSheets Integration
    When creating an instance of this class, is needed to inform the document name.
    Documents need to be shared with this email to be available:

    This class should handle all the interactions between the game information and users.
    """

    PLAYERS_KEYMAP = {
            'P1' : {
                'population' : 'C10',
                'minerals' : 'C11',
                'gas' : 'C12',
                'm_ships' : 'C15',
                'g_ships' : 'C16',
                'atk_ships' : 'C17'
            },
            'P2': {
                'population': 'F10',
                'minerals': 'F11',
                'gas': 'F12',
                'm_ships': 'F15',
                'g_ships': 'F16',
                'atk_ships': 'F17'
            },
            'P3': {
                'population': 'I10',
                'minerals': 'I11',
                'gas': 'I12',
                'm_ships': 'I15',
                'g_ships': 'I16',
                'atk_ships': 'I17'
            }
        }

    api_tab_name = 'API'
    api_location = 'Races Equilibrium'
    api_cell = 'J3'
    api_game_name = "SpaceCraft"

    dinasty_turn_cell = 'G19'

    config = {
        "type": "service_account",
        "project_id": "gsheetmultiplayergame",
        "private_key_id": "5323b3b1e4c91bec8a2e0615f67ba5c398d75136",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDCWZagCnUAblO7\nVIgjOHYblfrYAItwhZfFvnHSyfy9Omms84nPoMEiEbyrkUMFeBsRqQ59tFn3OdY4\nRw1vMUhN3ZtCC9vJ92xZ+xhTTlqWlV1dvlWFbc+DWuRjwZwm0Nk0paQpcrmwosNM\nIDeDKHQuk1VYHcWTunRoKQGAj+j3o5hLQ9nsfzP9Jd3foMr+mgYaWd2wCqQzF4Al\nu99C2byqwx+WIQal21bc+LwsE3qyqjL+C8ckwfrad51wIqTZ0IN03k+prBlPXQSu\nT84basjLtjJpDBLbFpArgwQZfzYopM+sSmKq/mjWVOe0DPJIDPCyMd0ae3Qp+pa1\nQ/zeapvbAgMBAAECggEAAvAg3MuXT2P+fMcH/9M23SOH1T3raVoNHGdBKxA6RPiY\nLdPf8gDafAgXhShzX3goEg5Gj84ZnVezwpt9dWkKljt7kqSS4uy6ysaG+CiEtbJq\nh9KfgLXHtvAWdCaD2ld00SK/LGH1m5NAI9QbCIwBpZ73G91bt3PQfwwPpZITAGzL\n6nk8Sr+Ekdig6r7rAbbqJqgM9+4A0Lj307rJ86/CbR4CcHJsXe8dXNj4jTtGp7J1\noOJT2E1lY3AinLj6PTXk/cZelHDFYckNdYvt6EG6lTxCRxUCy8pnTh/1DyXatWkO\nNa7git2m/aLKay+c/Q10Q96cKobhhbjOKNJR4hqakQKBgQD14J7KN4FRbTKs/mfu\nuXyaEz5o7Hnljy42KBojedcDXnF91+AiTRdaEwugZL/UYj735RNFfId3yYqE0bn1\nH8UNB2g+2ufX0x8qVgh87AvRjXYWLIGjGiB69X8ymo6gXS3L6RhspLuRANjaIYen\nkmCuHtHzobqYsxrXRoSmKZ+79QKBgQDKWedjhoeTMAim6sFDdwd4NnWFlpac3HxK\ns/6CcHqXJrchshjvh6VNdw8vISbz9RTdrkm8gK2+GACgmGhMB/+2UDdZIx/eKhmv\nS9h9KIMEql8OQ/Wty+0/x8DAlDiY5cnMspyk0EbHkxATi4Mh8ioEUAM1ha86BcC5\nU9gmiPlmjwKBgCJgjHMDfa4v0VUEoO1su7IjHKe44HYrJa/mvXjWUSykaMPKigjh\ntHEglpCPZY7BScKJIb+mYJ5r7FUTqadPENL4hSe8nYu8dfAKZVdp/WEIIUmKYXm3\nbnEin+0oVOaxAHUxGvwdsCfe8XLWG0xfl+rgXkRtCVTOPeN5dZRx32Z9AoGAA1zF\nFIlKvW5h5mwmM/nJXP0CrOqYrBiZ1B/zjbVSxCo3hs7PzUMiwwvEa9MQM6OR6jEY\nNpKo0GzTrdd6fDDx1dS1ZrzHrchjTt9ixImky7INDE6iyXWHBrVKBakw25GN7eHV\n6oMveed+r+R0lF7SxemSdBQ5miw4TJwRDmreQg8CgYAaVUvtnUyaMQhEFgr8VUEh\ns3CaTWEegsmvbRWnEHpF62JNMRTmXzfjs9p3rNKi+MQenKDWjhwBtJ+0xdOb0nkL\ncFtDQ5e04mgPHB4qn3XnRP6sStdK+4zojEtYgl0a+ZNo+Guybivd/HHhPKfm7kK1\njtqughkCrVBfmJvko/pZqQ==\n-----END PRIVATE KEY-----\n",
        "client_email": "gsheet-multiplayer-game@gsheetmultiplayergame.iam.gserviceaccount.com",
        "client_id": "104139155936314354024",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gsheet-multiplayer-game%40gsheetmultiplayergame.iam.gserviceaccount.com"
    }  # Configuration got from google API console (google sheets API)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(config, scope)
    client = gspread.authorize(creds)

    sheet = []

    def open_sheet(self, sheet_name, tab_name: str):
        """Opens the Sheet and defines tab"""
        self.sheet = self.client.open(sheet_name).worksheet(tab_name)

    def read_cell(self, cell: str):
        """Gets value from informed cell. Example -> A6 """
        return self.sheet.acell(cell).value

    def write_cell(self, cell: str, content):  # NOT IN USE
        """Writes value to informed cell. Example ('test', 'A6')"""

        self.sheet.update_acell(cell, content)

    def get_json(self, sheet_name, tab_name, cell):
        self.open_sheet(sheet_name, tab_name)
        return json.loads(self.read_cell(cell))

    def get_game_data(self):
        return self.get_json(self.api_game_name,self.api_location,self.api_cell)

    def change_turn_field(self, next_player_code):
        self.open_sheet(self.api_game_name, 'SERVER')
        self.write_cell(self.dinasty_turn_cell, next_player_code)

    def overwrite_property(self, position: str, property: str, value: int):
        self.open_sheet(self.api_game_name, 'Dinasty')
        self.write_cell(self.PLAYERS_KEYMAP[position][property], value)
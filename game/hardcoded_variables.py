# HARDCODED VARIABLES
EXTINCT = 'Extinct'
PLAYING = 'Playing'

P1 = 'P1'
P2 = 'P2'
P3 = 'P3'

ATK_SHIP_KEYWORDS = ['atk ships', 'as', 'attack ships', 'attack']
MINING_SHIP_KEYWORDS = ['mining ships', 'ms', 'mining', 'miners']
EXTRACTOR_SHIP_KEYWORDS = ['gas extractors', 'gas ships', 'gas']

EXTRACTOR = 'Extractor'
MINING = 'Mining'
ATTACK = 'Attack'

YES_GROUP = ['yes', 'si', 'sim', 'yeah', 'sure']
NO_GROUP = ['no', "don't", 'not', 'no way']

ATTACK_GROUP = ['attack', 'atk', 'deboxar', 'atacar']
REFRESH_GROUP = ['ref', 'refresh', 'is my turn?']
EXTRACT_GROUP = ['extract_gas', 'get gas', 'extract']
MINE_GROUP = ['mine', 'gather-minerals']
HANGAR_GROUP = ['hangar', 'buy', 'go to hangar']

ACTIONS_GROUP = []
for group in [ATTACK_GROUP, REFRESH_GROUP, EXTRACT_GROUP, MINE_GROUP, HANGAR_GROUP]:
    for item in group:
        ACTIONS_GROUP.append(item)

print(ACTIONS_GROUP)
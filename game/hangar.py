from .gsheet import GSheet
from .hardcoded_variables import ATK_SHIP_KEYWORDS, MINING_SHIP_KEYWORDS, EXTRACTOR_SHIP_KEYWORDS, EXTRACTOR, MINING, \
    ATTACK, YES_GROUP


class Hangar(GSheet):

    def check_amount(self, cmd):
        amount = self._integer_regex(cmd)
        if amount > 0:
            return amount
        else:
            print("Please provide a value in the command!")
            self.ship_market()

    def check_ship_type(self, cmd):
        for keyword in ATK_SHIP_KEYWORDS:
            if keyword in cmd:
                return ATTACK
        for keyword in MINING_SHIP_KEYWORDS:
            if keyword in cmd:
                return MINING
        for keyword in EXTRACTOR_SHIP_KEYWORDS:
            if keyword in cmd:
                return EXTRACTOR
        print("Please inform the shiptype in the command!")

    def ship_market(self):
        command = input('Welcome to the Hangar, what do you want?\n -> ')

        cmd = command.split(" ")
        amount = self.check_amount(cmd)
        ship_type = self.check_ship_type(cmd)

        if 'buy' in cmd:
            if ship_type == MINING:
                answer = input('Do you want to buy {amount}x Mining Ships?\n -> ')
                if answer in YES_GROUP:
                    my_miners = self.my_info()['m_ships']
                    self.overwrite_property(self.position, 'm_ships', my_miners + amount)

        if 'sell' in cmd:
            pass

    def buy_atk_ships(self):
        print('bought 100x')
        pass

    def buy_mining_ships(self):
        print('bought x50')
        pass

    def buy_gas_extractor(self):
        print('bought x125')
        pass

    def _integer_regex(self, cmd):
        for word in cmd:
            try:
                return int(word)
            except:
                pass



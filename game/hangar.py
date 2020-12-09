from .gsheet import GSheet
from .hardcoded_variables import ATK_SHIP_KEYWORDS, MINING_SHIP_KEYWORDS, EXTRACTOR_SHIP_KEYWORDS, EXTRACTOR, MINING, \
    ATTACK, YES_GROUP
from .instances import dinasty, press_key_to_continue
from .price import Price


class Hangar(GSheet):

    def check_amount(self, cmd):
        amount = self._integer_regex(cmd)
        if amount > 0:
            return amount
        else:
            print("Please provide a value in the command!")
            self.ship_market()

    def _check_ship_type(self, cmd):
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
        dinasty.get_response(False)
        command = input('Welcome to the Hangar, what do you want?\n -> ')

        cmd = command.split(" ")
        if 'prices' not in cmd:
            amount = self.check_amount(cmd)
        ship_type = self._check_ship_type(cmd)

        if 'buy' in cmd:
            if ship_type == MINING:
                can_buy, mineral_cost, gas_cost = self.check_can_buy(amount, 'mining_ship')
                if can_buy:
                    answer = input(f'Do you want to buy {amount}x Mining Ships?\n -> ')
                    if answer in YES_GROUP:
                        self._buy_mining_ships(amount, mineral_cost, gas_cost)

            elif ship_type == EXTRACTOR:
                can_buy, mineral_cost, gas_cost = self.check_can_buy(amount, 'gas_ship')
                if can_buy:
                    answer = input(f'Do you want to buy {amount}x Gas Extractors?\n -> ')
                    if answer in YES_GROUP:
                        self._buy_gas_extractor(amount, mineral_cost, gas_cost)

            elif ship_type == ATTACK:
                can_buy, mineral_cost, gas_cost = self.check_can_buy(amount, 'attack_ship')
                if can_buy:
                    answer = input(f'Do you want to buy {amount}x Attack Ships?\n -> ')
                    if answer in YES_GROUP:
                        self._buy_atk_ships(amount, mineral_cost, gas_cost)

        if 'prices' in cmd:
            print("Of course my man, here is our prices!\n")
            for ship_data in self.prices.items():
                print(" > ", ship_data[0], Price(ship_data[1]))

            press_key_to_continue()
            self.ship_market()

    def _buy_atk_ships(self, amount, mineral_cost, gas_cost):
        my_fighters = int(self.my_info()['attack_ships'])
        my_minerals = int(self.my_info()['minerals'])
        my_gas = int(self.my_info()['gas'])

        self.overwrite_property(self.position, 'attack_ships', my_fighters + amount)
        self.overwrite_property(self.position, 'minerals', my_minerals - mineral_cost)
        self.overwrite_property(self.position, 'gas', my_gas - gas_cost)

        print(f'[LOG] {amount}x Attack Ships Acquired!')

    def _buy_mining_ships(self, amount, mineral_cost, gas_cost):
        my_miners = int(self.my_info()['mining_ships'])
        my_minerals = int(self.my_info()['minerals'])
        my_gas = int(self.my_info()['gas'])

        self.overwrite_property(self.position, 'mining_ships', my_miners + amount)
        self.overwrite_property(self.position, 'minerals',  my_minerals - mineral_cost)
        self.overwrite_property(self.position, 'gas', my_gas - gas_cost)
        print(f'[LOG] {amount}x Mining Ships Acquired!')

    def _buy_gas_extractor(self, amount, mineral_cost, gas_cost):
        my_extractors = self.my_info()['mining_ships']
        self.overwrite_property(self.position, 'mining_ships', my_extractors + amount)
        self.overwrite_property(self.position, 'minerals', int(self.my_info()['minerals']) - mineral_cost)
        self.overwrite_property(self.position, 'gas', int(self.my_info()['gas']) - gas_cost)
        print(f'[LOG] {amount}x Gas Extractors Acquired!')

    def _integer_regex(self, cmd):
        for word in cmd:
            try:
                return int(word)
            except:
                pass

    def check_can_buy(self, amount, ship_name) -> dict:
        myinfo = self.my_info()
        my_gas = int(myinfo['gas'])
        my_minerals = int(myinfo['minerals'])
        ship_cost = Price(self.prices[ship_name])

        mineral_t_cost = ship_cost.minerals * amount
        gas_t_cost = ship_cost.gas * amount

        # DEBUG

        if my_gas > gas_t_cost and my_minerals > mineral_t_cost:
            return True, mineral_t_cost, gas_t_cost

        else:
            if my_gas < gas_t_cost:
                print(f"[LOG] You don't have enough gas! Needed : {gas_t_cost}G")
                press_key_to_continue()
                return False, gas_t_cost, mineral_t_cost
            else:
                print(f"[LOG] You don't have enough minerals! Needed {mineral_t_cost}M")
                press_key_to_continue()
                return False, gas_t_cost, mineral_t_cost

class Price:

    def __init__(self, price_string):
        cp = self.convert(price_string)
        self.minerals = cp[0]
        self.gas = cp[1]

    def convert(self, value):
        value = value.split(',')
        return [int(value[0]), int(value[1])]

    def __repr__(self):
        return f"COST : {self.minerals}M & {self.gas}G"
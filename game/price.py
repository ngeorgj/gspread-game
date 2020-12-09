class Price:

    def __init__(self, price_string):
        cp = self.convert(price_string)
        self.minerals = cp[0]
        self.gas = cp[1]

    def convert(self, value):
        value = value.split(',')
        return [value[0], value[1]]

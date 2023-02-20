from stockbuilder import StockBuilder


class Horizontal(StockBuilder) :
    def __init__(self , type) :
        self.type = type
        self.income = None
        self.balance = None

    def get_income(self) :
        print('Horizontal.get_income')

    def get_balance(self) :
        print('Horizontal.get_balance')

    def set_income(self) :
        print('Horizontal.set_income')

    def set_balance(self) :
        print('Horizontal.get_balance')
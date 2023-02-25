import pandas as pd
from utility import Utility


class StockBuilder:
    _horizontal = ['income', 'balance']
    _income_df = None
    _cash_df = None
    _balance_df = None
    is_start_col = None
    bs_start_col = None
    cf_start_col = None

    def __init__(self, sticker_name: str):
        print('StockBuilder')
        self.sticker_name = sticker_name
        self.share_price_in = Utility.share_price_in
    
    def get_income_df(self):
        return self._income_df

    def set_income_df(self):
        self._income_df = pd.read_excel(
            'data/'+self.sticker_name+'/'+self.sticker_name+'-income.xls')
        self.set_df_column('income')
        self.is_start_col = self._income_df.columns[1]
        self.cleanup_df('income')
        self._income_df = Utility.transform_income(
            self._income_df, self.is_start_col)

    def get_balance_df(self):
        return self._balance_df

    def set_balance_df(self):
        self._balance_df = pd.read_excel(
            'data/'+self.sticker_name+'/'+self.sticker_name+'-balance.xls')
        self.set_df_column('balance')
        self.bs_start_col = self._balance_df.columns[1]
        self.cleanup_df('balance')
        self._balance_df = Utility.transform_balance(
            self._balance_df, self.bs_start_col)

    def get_cash_df(self):
        return self._cash_df

    def set_cash_df(self):
        self._cash_df = pd.read_excel(
            'data/'+self.sticker_name+'/'+self.sticker_name+'-cashflow.xls')
        self.set_df_column('cash')
        self.cf_start_col = self._cash_df.columns[1]
        self.cleanup_df('cash')
        self._cash_df = Utility.transform_cash(
            self._cash_df, self.cf_start_col)

    def set_df_column(self, type):
        columns = None
        if type == 'income':
            columns = self._income_df.columns.values
            columns[0] = Utility.particulars
            self._income_df.columns = columns
        if type == 'balance':
            columns = self._balance_df.columns.values
            columns[0] = Utility.particulars
            self._balance_df.columns = columns
        if type == 'cash':
            columns = self._cash_df.columns.values
            columns[0] = Utility.particulars
            self._cash_df.columns = columns

    def get_df_column(self, type):
        if type == 'income':
            return self._income_df.columns
        elif type == 'balance':
            return self._balance_df.columns
        elif type == 'cash':
            return self._cash_df.columns

    def cleanup_df(self, type):
        if type == 'income':
            self._income_df.dropna(
                how='all', subset=self._income_df.columns[1:], inplace=True)
            self._income_df.fillna(0, inplace=True)
        elif type == 'balance':
            self._balance_df.dropna(
                how='all', subset=self._balance_df.columns[1:], inplace=True)
            self._balance_df.fillna(0, inplace=True)
        elif type == 'cash':
            self._cash_df.dropna(
                how='all', subset=self._cash_df.columns[1:], inplace=True)
            self._cash_df.fillna(0, inplace=True)
import pandas as pd
from utility import Utility
import time

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
        print(123)
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


class Vertical(StockBuilder) :

    def __init__(self , sticker_name) :
        super().__init__(sticker_name)
        self._va_income = None
        self._va_balance = None
    
    def get_va_revenue(self) :
        df = self.get_income_df()
        total_revenue_filter = df[Utility.particulars].apply(lambda x: x.strip()).eq('Total Revenue')
        return df.loc[total_revenue_filter,self.is_start_col:]
        
    def get_va_total_assets(self) :
         df = self.get_balance_df()
         total_assets_filter = df[Utility.particulars].apply(lambda x: x.strip()).eq('Total Assets')
         return df.loc[total_assets_filter,self.is_start_col:]

    def get_va_income_df(self) :
        return self._va_income
    
    def set_va_income_df(self) :
        self.set_income_df()
        df = self.get_income_df()
        start_col = self.is_start_col
        self._va_income = Utility.get_va_df(df,'income')
        revenue = self.get_va_revenue()
        transformed_income_df = df.loc[:Utility.get_basic_eps_pos(df),start_col:]
        self._va_income.loc[:Utility.get_basic_eps_pos(df),start_col:] = Utility.vertical_analysis(transformed_income_df,revenue)
        self._va_income.reset_index(drop=True , inplace=True)

    def get_va_balance_df(self) :
        return self._va_balance

    def set_va_balance_df(self) :
        self.set_balance_df()
        df = self.get_balance_df()
        start_col = self.bs_start_col
        self._va_balance = Utility.get_va_df(df,'balance')
        total_assets = self.get_va_total_assets()
        self._va_balance.loc[:,start_col:] =  Utility.vertical_analysis(self._va_balance.loc[:,start_col:],total_assets)
        self._va_balance.reset_index(drop=True , inplace=True)


class Horizontal(StockBuilder) :
    def __init__(self , sticker_name) :
        super().__init__(sticker_name)
        self._ha_income = None
        self._ha_balance = None
        self._ha_cash = None

    def get_ha_income(self) :
        print('Horizontal.get_income')
        return self.get_income_df()

    def set_ha_income(self) :
        self.set_income_df()
        df = self.get_income_df()
        start_col = self.is_start_col
        print('Horizontal.set_income')
        
    def get_ha_balance(self) :
        print('Horizontal.get_balance')

    def set_ha_balance(self) :
        print('Horizontal.set_balance')

    def get_ha_cash(self) :
        print('Horizontal.get_cash')

    def set_ha_cash(self) :
        print('Horizontal.set_cash')           

start_time = time.time()       
va = Vertical('mastek')
va.set_va_income_df()
print(va.get_va_income_df())

va.set_va_balance_df()
print(va.get_va_balance_df())

ha = Horizontal('mastek')
print(ha.get_ha_income())
print("--- %s seconds ---" % (time.time() - start_time))



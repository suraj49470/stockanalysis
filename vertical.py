from stockbuilder import StockBuilder
from utility import Utility

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
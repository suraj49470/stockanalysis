from stockbuilder import StockBuilder
from utility import Utility


class Trend(StockBuilder) :
        
        def __init__(self , sticker_name) :
            super().__init__(sticker_name)
            self._trend_income = None
            self._trend_balance = None
            self._trend_cash = None
        
        def get_is_trend_base(self) :
              start_col = self.is_start_col
              df  = self.get_income_df()
              return df[start_col]
        
        def get_bs_trend_base(self) :
              start_col = self.bs_start_col
              df  = self.get_balance_df().loc[:Utility.get_bl_last_pos(self.get_balance_df())]
              return df[start_col]
        
        def get_cf_trend_base(self) :
              temp_df = self.get_cash_df()
              temp_df_filt = temp_df[Utility.particulars].apply(Utility.count_leading_space).isin([0,8,12])
              temp_df = temp_df[temp_df_filt].copy()
              start_col = self.cf_start_col
              return temp_df[start_col]
        
        def get_trend_income(self) :
              return self._trend_income
        
        def get_trend_balance(self) :
              return self._trend_balance
        
        def get_trend_cash(self) :
              return self._trend_cash
        
        def set_trend_income(self) :
              self.set_income_df()
              df = self.get_income_df()
              start_col = self.is_start_col
              self._trend_income = Utility.get_trend_df(df,start_col,'income')
              for index , column in enumerate(self._trend_income.columns) :
                    if index < 2 :
                        pass
                    else:
                        self._trend_income.loc[:,column] = Utility.calculate_growth_series(df.loc[:,column],self.get_is_trend_base())
              self._trend_income.reset_index(inplace=True,drop=True) 

        def set_trend_balance(self) :
              self.set_balance_df()
              df = self.get_balance_df()
              start_col = self.bs_start_col
              self._trend_balance = Utility.get_trend_df(df,start_col,'balance')
              temp_df = df.loc[:Utility.get_bl_last_pos(df)]
              for index , column in enumerate(self._trend_balance.columns) :
                    if index < 2 :
                        pass
                    else:
                        self._trend_balance.loc[:,column] = Utility.calculate_growth_series(temp_df.loc[:,column],self.get_bs_trend_base()) 
              self._trend_balance.reset_index(inplace=True,drop=True)          

        def set_trend_cash(self) :
              self.set_cash_df()
              df = self.get_cash_df()
              start_col = self.cf_start_col
              temp_df_filt = df[Utility.particulars].apply(Utility.count_leading_space).isin([0,8,12])
              temp_df = df[temp_df_filt].copy()
              self._trend_cash = Utility.get_trend_df(temp_df,start_col,'cash')
              for index , column in enumerate(self._trend_cash.columns) :
                    if index < 2 :
                        pass
                    else:
                        self._trend_cash.loc[:,column] = Utility.calculate_growth_series(temp_df.loc[:,column],self.get_cf_trend_base())
              self._trend_cash.reset_index(inplace=True,drop=True)
              
from stockbuilder import StockBuilder
from utility import Utility

class Horizontal(StockBuilder) :
    def __init__(self , sticker_name) :
        super().__init__(sticker_name)
        self._ha_income = None
        self._ha_balance = None
        self._ha_cash = None

    def get_ha_income(self) :
        print('Horizontal.get_income')
        return self._ha_income

    def set_ha_income(self) :
        self.set_income_df()
        df = self.get_income_df()
        self._ha_income = Utility.get_ha_df(df,'income')
        temp_ha_filt = df[Utility.particulars].apply(Utility.count_leading_space).isin([0,4])
        for index , column in enumerate(self._ha_income.columns) :
            if index < 2 :
                pass;
            else:
                prevColumn = df.columns[index-1]
                self._ha_income.loc[temp_ha_filt,column] = Utility.calculate_growth_series(df.loc[temp_ha_filt,column],df.loc[temp_ha_filt,prevColumn])
        self._ha_income = self._ha_income[temp_ha_filt]
                
              
    def get_ha_balance(self) :
        print('Horizontal.get_balance')
        return self._ha_balance

    def set_ha_balance(self) :
        print('Horizontal.set_balance')
        self.set_balance_df()
        df = self.get_balance_df()
        self._ha_balance = Utility.get_ha_df(df,'balance')
        for index , column in enumerate(self._ha_balance.columns) :
            if index < 2 :
                pass;
            else:
                prevColumn = self._ha_balance.columns[index-1]
                self._ha_balance.loc[:,column] = Utility.calculate_growth_series(df.loc[:,column],df.loc[:,prevColumn])
        self._ha_balance[self.bs_start_col] = 0.0

                    

    def get_ha_cash(self) :
        print('Horizontal.get_cash')
        return self._ha_cash

    def set_ha_cash(self) :
        print('Horizontal.set_cash')           
        self.set_cash_df()
        df = self.get_cash_df()
        self._ha_cash = Utility.get_ha_df(df,'cash')
        cash_flow_stmt_ha_temp = self._ha_cash.copy()
        for index , column in enumerate(self._ha_cash.columns) :
            if index < 2 :
                pass
            else:
                prevColumn = self._ha_cash.columns[index-1]
                self._ha_cash.loc[:,column] = Utility.calculate_growth_series(cash_flow_stmt_ha_temp.loc[:,column],cash_flow_stmt_ha_temp.loc[:,prevColumn])
        self._ha_cash[self.cf_start_col] = 0.0

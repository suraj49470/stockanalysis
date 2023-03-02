from stockbuilder import StockBuilder
import pandas as pd
from utility import Utility

class Efficiency(StockBuilder) :

    def __init__(self , sticker_name) :
      super().__init__(sticker_name)
      self._efficiency = None
      self.set_balance_df()
      self.set_income_df()
    
    def set_efficiency_df(self) :
       bl_is_col_diff = len(self.get_balance_df().columns) - len(self.get_income_df().columns)
       self._efficiency = pd.DataFrame(columns=self.get_balance_df().columns)
       self._efficiency[Utility.particulars] = ['Total asset turnover' , 'Net fixed asset turnover' , 'Equity turnover']
       operating_efficiency_total_revenue = Utility.get_df_items(self.get_income_df(),'Total Revenue' , self.is_start_col).iloc[:,:bl_is_col_diff]
       operating_efficiency_total_assets = Utility.get_df_items(self.get_balance_df(),'Total Assets' , self.bs_start_col)
       operating_efficiency_ppe = Utility.get_df_items(self.get_balance_df(),'Net Property, Plant and Equipment' , self.bs_start_col)
       operating_efficiency_equity = Utility.get_df_items(self.get_balance_df(),'Equity Attributable to Parent Stockholders' , self.bs_start_col)
       for i , column in enumerate(self.get_balance_df().columns):
            if i > 1 :
                prevColumn = self.get_balance_df().columns[i-1]
                ta_mean = operating_efficiency_total_assets.loc[:,prevColumn:column].mean(axis=1)
                ppe_mean = operating_efficiency_ppe.loc[:,prevColumn:column].mean(axis=1)
                equity_mean = operating_efficiency_equity.loc[:,prevColumn:column].mean(axis=1)
                self._efficiency.loc[0:0,column] = Utility.calculate_ratio(operating_efficiency_total_revenue.loc[:,column],ta_mean).values
                self._efficiency.loc[1:1,column] = Utility.calculate_ratio(operating_efficiency_total_revenue.loc[:,column],ppe_mean).values
                self._efficiency.loc[2:2,column] = Utility.calculate_ratio(operating_efficiency_total_revenue.loc[:,column],equity_mean).values
       self._efficiency.dropna(how='all' , axis=1,inplace=True)
    
    def get_efficiency_df(self) :
        return self._efficiency

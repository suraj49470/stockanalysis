from stockbuilder import StockBuilder
import pandas as pd
from utility import Utility

class Solvency(StockBuilder) :

    def __init__(self , sticker_name) :
      super().__init__(sticker_name)
      self.set_balance_df()
      self._solvency_ratio = pd.DataFrame(columns=self.get_balance_df().columns)
      self._solvency_ratio[Utility.particulars] = ['current ratio' , 'quick ratio', 'cash ratio']

    def get_current_assets(self) :
       return Utility.get_df_items(self.get_balance_df() , 'total current assets' , self.bs_start_col)
    
    def get_current_liabilities(self) :
       return Utility.get_df_items(self.get_balance_df() , 'total current liabilities', self.bs_start_col)
    
    def get_inventories(self) :
       temp_inventories = Utility.get_df_items(self.get_balance_df() , 'inventories' , self.bs_start_col)
       if len(temp_inventories.value_counts().values) == 0 :
            data = [[0] * len(temp_inventories.columns)]
            return pd.DataFrame(data=data , columns=temp_inventories.columns).copy()
       return temp_inventories
        
    
    def get_cash_equivalents(self) :
       return Utility.get_df_items(self.get_balance_df() , 'cash and cash equivalents', self.bs_start_col)
    
    def get_quick_assets(self) :
       return self.get_current_assets() - self.get_inventories().values
    
    def get_solvency(self) :
       return self._solvency_ratio
    
    def set_current_ratio(self) :
       self._solvency_ratio.loc[0:0,self.bs_start_col:] = Utility.calculate_ratio(self.get_current_assets(),self.get_current_liabilities()).values
    
    def set_quick_ratio(self) :
       self._solvency_ratio.loc[1:1,self.bs_start_col:] = Utility.calculate_ratio(self.get_quick_assets(),self.get_current_liabilities()).values

    def set_cash_ratio(self) :
       self._solvency_ratio.loc[2:2,self.bs_start_col:] = Utility.calculate_ratio(self.get_cash_equivalents(),self.get_current_liabilities()).values  
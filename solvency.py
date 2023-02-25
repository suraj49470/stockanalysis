from stockbuilder import StockBuilder
import pandas as pd
from utility import Utility

class Solvency(StockBuilder) :

    def __init__(self , sticker_name) :
      super().__init__(sticker_name)
      self.set_income_df()

    def get_current_assets(self) :
       return Utility.get_df_items(self.get_income_df() , 'total current assets' , self.bs_start_col)
    
    def get_current_liabilities(self) :
       return Utility.get_df_items(self.get_income_df() , 'total current liabilities', self.bs_start_col)
    
    def get_inventories(self) :
       temp_inventories = Utility.get_df_items(self.get_income_df() , 'inventories' , self.bs_start_col)
       if len(temp_inventories.value_counts().values) == 0 :
            data = [[0] * len(temp_inventories.columns)]
            return pd.DataFrame(data=data , columns=temp_inventories.columns).copy()
       return temp_inventories
        
    
    def get_cash_equivalents(self) :
       return Utility.get_df_items(self.get_income_df() , 'cash and cash equivalents', self.bs_start_col)
    
    def get_quick_assets(self) :
       return self.get_current_assets() - self.get_inventories().values
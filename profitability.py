from stockbuilder import StockBuilder
import pandas as pd
from utility import Utility

class Profitability(StockBuilder) :

    def __init__(self , sticker_name) :
      super().__init__(sticker_name)
      self._profitability = None
      self.set_balance_df()
      self.set_income_df()
      
    
    def set_profitability_df(self) :
      self._profitability = pd.DataFrame(columns=self.get_income_df().columns)
      self._profitability[Utility.particulars] = ['Gross profit margin' , 'Operating profit margin', 'Net profit margin' , 'Return on total assets','Return on total equity','Return on owners equity']
      self.operating_profitability_gross_profit = Utility.get_df_items(self.get_income_df(),'Gross Profit' , self.is_start_col).apply(abs)
      self.operating_profitability_revenue = Utility.get_df_items(self.get_income_df(),'Total Revenue' , self.is_start_col).apply(abs)
      self.operating_income_expense = Utility.get_df_items(self.get_income_df(),'Operating Income/Expenses' , self.is_start_col).apply(abs)
      self.other_operating_income_expense = Utility.get_df_items(self.get_income_df(),'Other Income/Expense, Operating' , self.is_start_col).apply(abs)
      self.EBIT = self.operating_profitability_gross_profit - (self.operating_income_expense - self. other_operating_income_expense)
      self.net_income = Utility.get_df_items(self.get_income_df(),'Net Income before Extraordinary Items and Discontinued Operations' , self.is_start_col)
      self.net_income_owners = Utility.get_df_items(self.get_income_df(),'Net Income after Non-Controlling/Minority Interests' , self.is_start_col)
      self.operating_profitability_total_assets = Utility.get_df_items(self.get_balance_df(),'Total Assets' , self.bs_start_col)
      self.total_equity = Utility.get_df_items(self.get_balance_df(),'Total Equity' , self.bs_start_col)
      self.total_owners_equity = Utility.get_df_items(self.get_balance_df(),'Equity Attributable to Parent Stockholders' , self.bs_start_col)
        
    
    def set_profitablity_ratio(self) :
       self._profitability.loc[0:0,self.is_start_col:] = Utility.calculate_ratio(self.operating_profitability_gross_profit,self.operating_profitability_revenue).values
       self._profitability.loc[1:1,self.is_start_col:] = Utility.calculate_ratio(self.EBIT,self.operating_profitability_revenue).values
       self._profitability.loc[2:2,self.is_start_col:] = Utility.calculate_ratio(self.net_income,self.operating_profitability_revenue).values
       self.operating_profitability_balance_columns = self.get_balance_df().loc[:,self.is_start_col:].columns
       for i , column in enumerate(self.operating_profitability_balance_columns) :
            if i > 0 :
                prevColumn = self.operating_profitability_balance_columns[i-1]
                assets_mean = self.operating_profitability_total_assets.loc[:,prevColumn:column].mean(axis=1)
                equity_mean = self.total_equity.loc[:,prevColumn:column].mean(axis=1)
                owners_equity_mean = self.total_owners_equity.loc[:,prevColumn:column].mean(axis=1)
                self._profitability.loc[3:3,column] = Utility.calculate_ratio(self.EBIT.loc[:,column],assets_mean).values
                self._profitability.loc[4:4,column] = Utility.calculate_ratio(self.net_income.loc[:,column],equity_mean).values
                self._profitability.loc[5:5,column] = Utility.calculate_ratio(self.net_income_owners.loc[:,column],owners_equity_mean).values
       self._profitability.fillna('-' , inplace=True)
            
        
        

    def get_profitability_df(self) :
        return self._profitability

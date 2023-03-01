from stockbuilder import StockBuilder
import pandas as pd
from utility import Utility

class Turnover(StockBuilder) :

    def __init__(self , sticker_name) :
      super().__init__(sticker_name)
      self.set_balance_df()
      self.set_income_df()
      self.set_turnover_df()
      self._turnover_ratio.drop([self.bs_start_col] , inplace=True , axis=1)
      self.set_turnover_days_df()
      
    
    def set_turnover_df(self) :
       self._turnover_ratio = pd.DataFrame(columns=self.get_balance_df().columns)
       self._turnover_ratio[Utility.particulars] = ['Receivable turnover' , 'Inventory turnover', 'Payables turnover']
       self.set_account_receivable_turnover()
       self.set_account_payables_turnover()
       self.set_invetories_turnover()

       

    def set_turnover_days_df(self) :
       self._days_turnover_ratio = pd.DataFrame(columns=self._turnover_ratio.columns)
       self._days_turnover_ratio[Utility.particulars] = ['Receivable turnover days' , 'Inventory turnover days' , 'Payables turnover days']
       self._days_turnover_ratio.iloc[:,1:] = self._turnover_ratio.iloc[:,1:].applymap(Utility.days_turnover)
       
    def get_turnover_df(self) :
       return self._turnover_ratio
    
    
    def get_turnover_days_df(self) :
       return self._days_turnover_ratio
    
    def set_account_receivable_turnover(self) :
       account_receivables = Utility.get_df_items(self.get_balance_df(),'Trade and Other Receivables, Current' , self.bs_start_col)
       total_revenue = Utility.get_df_items(self.get_income_df(),'Total Revenue' , self.is_start_col,)
       for i , column in enumerate(self.get_balance_df().columns):
            if i > 1 :
                ar_mean = account_receivables.iloc[:,i-2:i].mean(axis=1)
                self._turnover_ratio.loc[0:0,column] = Utility.calculate_ratio(total_revenue.loc[:,column],ar_mean).values

    def get_puchase(self) :
       bl_is_col_diff = len(self.get_balance_df().columns) - len(self.get_income_df().columns)
       cogs_ap = Utility.get_df_items(self.get_income_df(),'Cost of Revenue',self.is_start_col).iloc[:,:bl_is_col_diff].apply(abs)
       invetories_ap = Utility.get_invetory(self.get_balance_df(),'Inventories',self.bs_start_col) 
       purchases = pd.DataFrame(data=[ [0] * len(invetories_ap.columns) ],columns=invetories_ap.columns.values)
       for i , column in enumerate(invetories_ap.columns) :
            if i > 0 :
                currentCol = column
                prevColumn = invetories_ap.columns[i-1]
                inventories_diff = invetories_ap[currentCol] - invetories_ap[prevColumn]
                purchases[currentCol] = cogs_ap[currentCol] + inventories_diff.values

       return purchases 
    
    def set_account_payables_turnover(self) :
        account_payables = Utility.get_df_items(self.get_balance_df(),'Payables and Accrued Expenses, Current',self.bs_start_col)
        purchases = self.get_puchase()
        for i , column in enumerate(self.get_balance_df().columns):
            if i > 1 :
                ap_mean = account_payables.iloc[:,i-2:i].mean(axis=1)
                self._turnover_ratio.loc[2:2,column] = Utility.calculate_ratio(purchases.loc[:,column],ap_mean).values
    
    def set_invetories_turnover(self) :
        cogs = Utility.get_df_items(self.get_income_df(),'Cost of Revenue' , self.is_start_col).apply(abs)
        invetories = Utility.get_invetory(self.get_balance_df(),'Inventories',self.bs_start_col)
        is_zero_invetories  = (invetories.loc[:,self.bs_start_col:] == 0).all(axis=1).values[0]
        for i , column in enumerate(self.get_balance_df().columns):
            if(is_zero_invetories) :
                self._turnover_ratio.loc[1:1,self.bs_start_col:] = '-'
                break
            elif i > 1 :
                inv_mean = invetories.iloc[:,i-2:i].mean(axis=1)
                self._turnover_ratio.loc[1:1,column] = Utility.calculate_ratio(cogs.loc[:,column],inv_mean).values

    def get_cash_conversion_cycle(self) :
        start_column = self.get_turnover_days_df().columns[1]
        receivable_days = Utility.get_df_items(self.get_turnover_days_df(),'Receivable turnover days',start_column)
        inventory_days = Utility.get_df_items(self.get_turnover_days_df(),'Inventory turnover days',start_column).replace({'-' : 0})
        payable_days = Utility.get_df_items(self.get_turnover_days_df(),'Payables turnover days',start_column)
        ccy = inventory_days + receivable_days - payable_days
        return pd.DataFrame(ccy) 

    
    
    
        




        


       
    
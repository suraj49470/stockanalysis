import re
import pandas as pd
class Utility :
    
    share_price_in = 1000000
    particulars = 'particulars'

    @staticmethod
    def calculate_growth(current , previous) :
        if current == 0 and previous == 0 or current == 0 and previous != 0:
            return 0
        if current != 0 and previous == 0 :
            return current / 100
        return ((current/previous) - 1) * 100
    
    @staticmethod
    def calculate_growth_series(curr_df,prev_df):
        temp_df = curr_df.copy()
        for index in curr_df.index :
            temp_df.loc[index] = round(Utility.calculate_growth(curr_df.loc[index],prev_df[index]),2)
        return temp_df
    
    @staticmethod
    def get_share_price_in(price) :
        return round((price / Utility.share_price_in),2)
    
    @staticmethod
    def get_share_price_in(price) :
       return round((price / Utility.share_price_in),2)
    
    @staticmethod
    def vertical_analysis(item , divider) :
        return round((item/divider.values) * 100 , 2)
    
    @staticmethod
    def count_leading_space(s): 
        match = re.search(r"^\s*", s) 
        return 0 if not match else match.end()
    
    @staticmethod
    def calculate_ratio(dividend , divisor) : 
        return dividend.div(divisor.values).apply(lambda x: round(x,2))
    
    @staticmethod
    def styles(color = 'white',backcolor = '#308D46'):
        return [dict(selector="caption",
                        props=[("text-align", "center"),
                                ("font-size", "150%"),
                                ("color", color),
                                ("background", backcolor),
                                ("font-weight", '600'),
                                ("text-transform", 'uppercase')
                                ])]
    
    @staticmethod
    def get_basic_eps_pos(df) :
            basic_eps_filter = df[Utility.particulars].eq('Basic EPS')
            return df[basic_eps_filter].index[0] - 1
    
    @staticmethod
    def get_bl_last_pos(df) :
           balance_sheet_ha_results_till = df[Utility.particulars].apply(lambda x: x.strip()).eq('Non-Controlling/Minority Interests in Equity')
           return df[balance_sheet_ha_results_till].index.values[0]
    
    @staticmethod
    def transform_income(income_statement , start_col) :
            temp_df = pd.DataFrame(income_statement)
            basic_eps_filter = income_statement[Utility.particulars].eq('Basic EPS')
            basic_eps_pos = income_statement[basic_eps_filter].index[0]
            WASO_filter = income_statement[Utility.particulars].isin(['Basic Weighted Average Shares Outstanding','Diluted Weighted Average Shares Outstanding','Basic WASO','Diluted WASO'])
            waso_pos = income_statement[WASO_filter].index
            temp_df.loc[0:basic_eps_pos,start_col:] = temp_df.loc[0:basic_eps_pos,start_col:].apply(Utility.get_share_price_in)
            temp_df.loc[waso_pos,start_col:] = temp_df.loc[waso_pos,start_col:].apply(Utility.get_share_price_in)
            temp_revenue = temp_df.loc[1]
            temp_df.loc[1] = temp_df.loc[0]
            temp_df.loc[0] = temp_revenue

            total_rev = temp_df[Utility.particulars].index == 0
            temp_df.loc[total_rev,Utility.particulars] = income_statement.loc[total_rev,Utility.particulars].values[0].strip() 
            return temp_df
    
    @staticmethod
    def transform_balance(balance_sheet , start_col) :
            temp_df = pd.DataFrame(balance_sheet)
            temp_df.loc[0:,start_col:] = temp_df.loc[0:,start_col:].applymap(Utility.get_share_price_in)
            total_equity_filter = temp_df[Utility.particulars].apply(lambda x: x.strip()).eq('Total Equity')
            total_equity_row = temp_df.loc[total_equity_filter,start_col:].index.values[0]
            total_liabilities_filter = temp_df[Utility.particulars].apply(lambda x: x.strip()).eq('Total Liabilities')
            total_liabilities_row = temp_df.loc[total_liabilities_filter,start_col:].index.values[0]
            temp_df.loc[total_liabilities_filter,start_col:] = temp_df.loc[[total_equity_row,total_liabilities_row],start_col:].sum().values
            return temp_df

    @staticmethod
    def transform_cash(cashflow_statement , start_col) :
            temp_df = pd.DataFrame(cashflow_statement)
            temp_df.loc[0:,start_col:] =  temp_df.loc[0:,start_col:].applymap(Utility.get_share_price_in)
            return temp_df
    
    @staticmethod
    def get_va_df(df, type) :
         temp_df = None
         if type == 'income':
              temp_df = pd.DataFrame(columns=df.columns)
              basic_eps_filter = df[Utility.particulars].eq('Basic EPS')
              basic_eps_pos = df[basic_eps_filter].index[0]
              temp_df[Utility.particulars] = df.loc[0:Utility.get_basic_eps_pos(df),Utility.particulars].copy()
              return temp_df
         elif type == 'balance' :
              bs_va_temp = df.loc[:Utility.get_bl_last_pos(df)]
              bs_va_temp = pd.DataFrame(bs_va_temp)
              filt = bs_va_temp[Utility.particulars].apply(Utility.count_leading_space).isin([0,4,8])
              return pd.DataFrame(bs_va_temp[filt])
              
         

    @staticmethod
    def get_ha_df(df, type) :
         temp_df = None
         if type == 'income':
                temp_df=  pd.DataFrame(columns= df.columns)
                temp_df[Utility.particulars] = df[Utility.particulars]
                temp_df.fillna(0 , inplace=True)
                return temp_df
         elif type == 'balance' :
              temp_df = df.loc[:Utility.get_bl_last_pos(df)]
              temp_df = pd.DataFrame(temp_df)
              filt = temp_df[Utility.particulars].apply(Utility.count_leading_space).isin([0,4,8])
              temp_df = pd.DataFrame(temp_df[filt])
              return temp_df
         elif type == 'cash' :
              cashflow_statement_filt = df[Utility.particulars].apply(Utility.count_leading_space).isin([0,8,12])
              temp_df = pd.DataFrame(df[cashflow_statement_filt])
              temp_df.reset_index(inplace=True, drop=True)
              return temp_df

    @staticmethod
    def get_trend_df(df, start_col, type) :
         temp_df = None
         if type == 'income':
                temp_df = pd.DataFrame(columns=df.columns)
                temp_df[Utility.particulars] = df[Utility.particulars]
                temp_df[start_col] = 0
                temp_df.fillna(0,inplace=True)
                return temp_df
         elif type == 'balance' :
              temp_balance = df.loc[:Utility.get_bl_last_pos(df)]
              temp_df = pd.DataFrame(columns=temp_balance.columns)
              temp_df[Utility.particulars] = temp_balance[Utility.particulars]
              temp_df[start_col] = 0
              temp_df.fillna(0,inplace=True)
              temp_balance = None
              return temp_df
         elif type == 'cash' :
              temp_df = pd.DataFrame(columns=df.columns)
              temp_df[Utility.particulars] = df[Utility.particulars]
              temp_df[start_col] = 0
              return temp_df
    
    @staticmethod
    def get_df_items(df , key_name , start_col) :
         filter = df[Utility.particulars].apply(lambda x: x.strip().lower()).eq(key_name)
         return df.loc[filter,start_col:].copy()


    
         
           
        

        
        


        
    
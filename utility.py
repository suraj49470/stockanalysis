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
        return ((current/previous) - 1)
    
    @staticmethod
    def calculate_growth_series(curr_df,prev_df):
        temp_df = curr_df.copy()
        for index in curr_df.index :
            temp_df.loc[index] = Utility.calculate_growth(curr_df.loc[index],prev_df[index])
        return temp_df
    
    @staticmethod
    def get_share_price_in(price) :
        return round((price / Utility.share_price_in),2)
    
    @staticmethod
    def get_share_price_in(price) :
       return round((price / Utility.share_price_in),2)
    
    @staticmethod
    def vertical_analysis(item , divider) :
        return item/divider
    
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
            total_assets_filter = temp_df[Utility.particulars].apply(lambda x: x.strip()).eq('Total Assets')
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
    def get_va_df(df , start_col , type) :
         print(start_col)
         temp_df = None
         if type == 'income':
              basic_eps_filter = df[Utility.particulars].eq('Basic EPS')
              basic_eps_pos = df[basic_eps_filter].index[0]
              temp_df = pd.DataFrame(columns=df.columns)
              temp_df[Utility.particulars] = temp_df.loc[0:basic_eps_pos - 1,Utility.particulars].copy()
              return temp_df
         elif type == 'balance' :
              pass
           
        

        
        


        
    
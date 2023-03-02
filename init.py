from stockbuilder import StockBuilder
from utility import Utility
from horizontal import Horizontal
from vertical import Vertical
from trend import Trend
from solvency import Solvency
from turnover import Turnover
from efficiency import Efficiency
from profitability import Profitability
import time

def init_reports(company) :

    va = Vertical(company)
    va.set_va_income_df()
    print(va.get_va_income_df())

    va.set_va_balance_df()
    print(va.get_va_balance_df())

    ha = Horizontal(company)
    ha.set_ha_income()
    print(ha.get_ha_income())

    ha.set_ha_balance()
    print(ha.get_ha_balance())

    ha.set_ha_cash()
    print(ha.get_ha_cash())


    tr = Trend(company)
    tr.set_trend_income()
    print(tr.get_trend_income())

    tr.set_trend_balance()
    print(tr.get_trend_balance())


    tr.set_trend_cash()
    print(tr.get_trend_cash())

    sl = Solvency(company)
    sl.set_current_ratio()
    sl.set_quick_ratio()
    sl.set_cash_ratio()
    print(sl.get_solvency())

    turnover = Turnover(company)
    print(turnover.get_turnover_df())
    print(turnover.get_turnover_days_df())
    print(turnover.get_cash_conversion_cycle())

    efficiency = Efficiency(company)
    efficiency.set_efficiency_df()
    print(efficiency.get_efficiency_df())

    profitability = Profitability(company)
    profitability.set_profitability_df()
    profitability.set_profitablity_ratio()
    print(profitability.get_profitability_df())




start_time = time.time()
init_reports('tcs')
print("--- %s seconds ---" % (time.time() - start_time))
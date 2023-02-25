from stockbuilder import StockBuilder
from utility import Utility
from horizontal import Horizontal
from vertical import Vertical
from trend import Trend
import time



start_time = time.time()       
# va = Vertical('mastek')
# va.set_va_income_df()
# print(va.get_va_income_df())

# va.set_va_balance_df()
# print(va.get_va_balance_df())

# ha = Horizontal('mastek')
# ha.set_ha_income()
# print(ha.get_ha_income())

# ha.set_ha_balance()
# print(ha.get_ha_balance())

# ha.set_ha_cash()
# print(ha.get_ha_cash())


tr = Trend('mastek')
# tr.set_trend_income()
# print(tr.get_trend_income())

tr.set_trend_balance()
print(tr.get_trend_balance())
print("--- %s seconds ---" % (time.time() - start_time))
from jqdatasdk import *
import pandas as pd


auth('18069298795','298795')





def get_futures():
    return get_all_securities(['futures'])

def set_pd():
    pd.set_option('display.max_columns', 10000000)
    pd.set_option('display.width', 10000000)
    pd.set_option('display.max_colwidth', 1000000)
    pd.set_option("display.max_rows",1000000)
set_pd()
#print(get_futures())


#ret=get_bars('rb2005.XSGE', 2000, unit='1m',fields=['date','open','high','low','close'],include_now=False,end_dt='2019-11-1')
ret=get_bars('M9999.XDCE', 100, unit='60m',fields=['date','open','high','low','close'],include_now=False,end_dt='2018-12-18')



# close=ret[['date','close']]
# close=close.rename(columns={"close": "close_price"})
# ma20=ret['close'].rolling(20).mean()

#ret=pd.concat([close,ma20],axis=1)


#print(ret.rename(columns={"close": "ma20"}))

#print(ret.dtypes)


#print(ret['close'])
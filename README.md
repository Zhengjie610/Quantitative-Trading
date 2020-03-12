# Quantitative-Trading
模拟量化交易

1、一个模拟交易的程序
2、可以通过买卖策略，同时卖开买开X手计算最后盈利。
3、运行 python3 buyANDsell.py

buy_amount = 2250 # 买开总手数
sell_amount = 2250# 卖开总手数
base_profits_points=10 #基准盈利点
close_unit=1  #每次平仓数
buy_sell_unit=1   #每次买卖数

4、比如同时开100手，(base_profits_points)设置每跌X点 就买入X手(buy_sell_unit)，每涨X点就卖出X手，同步进行。
5、close_unit 每次平仓X手，买卖通用。

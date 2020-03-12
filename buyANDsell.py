import time
import math
from finance import futures as f
import numpy as np
margin = 1  # 保证金

currentPrice = []  # 历史价格表，遍历的每一个都认为是当前价格

buy_amount = 2250 # 买开总手数
sell_amount = 2250# 卖开总手数

buyPrice = 0  # 平均买持仓价
sellPrice = 0  # 平均卖持仓价

buy_profits = 0
sell_profits = 0



sell_chicang = 0  # sell总持仓=sell手数*当前价格
buy_chicang = 0  # buy总持仓=buy手数*当前价格

unit = 10
close_unit=1  #每次平仓数
buy_sell_unit=1   #每次买卖数
sell_floating=0  #买卖浮动

buy_floating=0

base_profits_points=10 #基准盈利点


def check_double():
    if buy_amount/sell_amount >=buy_sell_unit:
        print('买单太多')
        exit()

    if sell_amount/buy_amount >=buy_sell_unit:
        print('卖单太多')
        exit()



def first_buy_sell():
    global sell_chicang
    global buy_chicang
    global buyPrice
    global sellPrice

    if len(currentPrice):
        sell_chicang = currentPrice[0] * sell_amount
        buy_chicang = currentPrice[0] * buy_amount
        buyPrice = currentPrice[0]
        sellPrice = currentPrice[0]  # 设置初始价格
        print('[1]')
        print('保证金：',sell_chicang*margin,'均买价：',buyPrice,'均卖价：', sellPrice,'总买：',buy_amount,'总卖：',sell_amount)
    else:
        print('没有输入价格参数')

def cut_line():
    print('-------------------------------------')

def get_current_position(current):

    print('当前价格：', current, '均买价：', buyPrice, '均卖价：', sellPrice, '买单总数：', buy_amount, '卖单总数：', sell_amount)


def check_has_profits():  # 买开，当前价格大于开仓价，平掉多单（卖平），然后卖开
    profits = []
    global unit
    global buy_sell_unit
    global base_profits_points
    for current in currentPrice[1:]:
        cut_line()
        print(current)
        #check_double()
        if current - buyPrice >= base_profits_points:
            # 如果买开赚到10点  这里指的是上一次基准价格i-1和i的价格
            print('执行卖平', buy_sell_unit, '手,', '执行卖开', buy_sell_unit, '手')
            close_buy(current)  # 卖平盈利
            sell(current)  # 同时卖开10手
            profit = (current - buyPrice) * unit * buy_sell_unit  # 利润计算 unit=10 1手1点10块钱
            profits.append(profit)
            update_floating(current)
            print('平仓盈利集合：', profits)
            print('利润总和', math.fsum(profits))

        elif (current - sellPrice) <= -base_profits_points:  # 卖开后，价格下跌，低于开仓10点，买平盈利，同时买开
            print('执行买平',buy_sell_unit,'手，','执行买开',buy_sell_unit,'手')
            close_sell(current)  # 买平获利
            buy(current)  # 买开10手
            profit = (current - sellPrice) * unit * buy_sell_unit  # 利润计算
            profits.append(abs(profit))
            update_floating(current)
            print('平仓盈利集合：', profits)
            print('利润总和', math.fsum(profits))

        else:
            print('利润没有超过十个点，继续执行！！！')
            #get_current_position(current)
            print('平仓盈利集合：', profits)
            print('利润总和', math.fsum(profits))
            update_floating(current)
            continue

def update_floating(curret_price):
    global sell_chicang
    global sell_amount
    global sellPrice
    global buy_chicang
    global buy_amount
    global buyPrice
    global buy_floating
    global sell_floating
    buy_floating_profits=buy_amount*unit*(curret_price-buyPrice)
    sell_floating_profits=sell_amount*unit*(sellPrice-curret_price)
    get_current_position(curret_price)
    print('多单盈亏：', buy_floating_profits, '空单盈亏：', sell_floating_profits)

def close_sell(current_price):
    global sell_chicang
    global sell_amount
    global close_unit

    if sell_amount >= close_unit:
        sell_amount = sell_amount - close_unit
    #elif sell_amount==0:
        #sell_amount=sell_amount+20
    else:
        print('没有可以买平的了')
        exit()


def close_buy(current_price):
    # 持仓和总手数一开始是确定好的。
    global close_unit
    global buy_chicang
    global buy_amount
    if buy_amount >= close_unit:
        buy_amount = buy_amount - close_unit
    #elif buy_amount==0:
        #buy_amount=buy_amount+20
    else:
        print('没有可以卖平的了')
        exit()

def buy(current_price):
    global buy_chicang
    global buy_amount
    global buyPrice
    global buy_floating
    global buy_sell_unit
    print('传进来的价格：',current_price)
    #print('之前的买单平均价', buyPrice, '之前的持仓保证金： ', buy_chicang * margin,'之前的总手数：', buy_amount)
    floating = (current_price - buyPrice) * buy_amount * unit  # 浮动盈亏计算
    buyPrice = ((buyPrice * buy_amount) + (buy_sell_unit * current_price)) / (buy_amount + buy_sell_unit)
    # print('新的买单平均价',buyPrice)
    buy_amount = buy_amount + close_unit
    buy_chicang = buyPrice * buy_amount

    #print('新的买单平均价: ', buyPrice, '新的保证金：', buy_chicang * margin, '新的总买手数：', buy_amount)
    print('多单保证金：', buy_chicang * margin)
    buy_floating=floating
    #print('多单盈亏：',buy_floating, '空单盈亏：',sell_floating)
def sell(current_price):
    global sell_chicang
    global sell_amount
    global sellPrice
    global sell_floating
    global buy_sell_unit
    #print('之前的卖单平均价: ', sellPrice, '之前的卖单持仓保证金：', sell_chicang * margin, '之前的总手数：', sell_amount)
    floating = (sellPrice-current_price) * sell_amount * unit  # 浮动盈亏计算 如果卖价-当前价格<0 就是亏 大于0就是赚钱
    sellPrice = (sell_amount * sellPrice + buy_sell_unit * current_price) / (sell_amount + buy_sell_unit)  # 新的平均持仓价格计算
    sell_amount = sell_amount + buy_sell_unit
    sell_chicang = sell_amount * sellPrice  # 总持仓=当前总手数*平均卖价

    #print('新的卖单平均价: ', sellPrice, '新的保证金：', sell_chicang * margin, '新的卖总手数: ', sell_amount)
    print('空单保证金：', sell_chicang * margin)
    sell_floating=floating
    #print('多单盈亏：', buy_floating, '空单盈亏：', sell_floating)
def set_currentPrice_list():
    global currentPrice
    #currentPrice = [3524,3514,3504,3534,3600,3525]
    currentPrice = np.array(f.ret['close']).tolist()
    print(currentPrice)







set_currentPrice_list()
first_buy_sell()
check_has_profits()
#print(f.ret['close'])




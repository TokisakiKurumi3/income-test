'''
    根据dict统计具体收益
'''

import time
from matplotlib import pyplot as plt
import mpl_finance as mpf
from matplotlib.pylab import date2num
import datetime

INIT_MONEY = 2000

def invest_one_game(game, money):  # game = [timeStamp(调整后时间戳), day, shouyi]

    # 1.固定投资
    # wangduzi = 100
    # # 2.固定比例
    # wangduzi = money * 0.04
    # # 3.分周中周末
    timeArray = time.localtime(game[0])
    if timeArray.tm_wday > 4:
        # wangduzi = money * 0.04
        wanduzi = 75
    else:
        # wanduzi = money * 0.07
        wanduzi = 125

    return wanduzi

def invest_one_day(day_dict, money):

    cur_money = money
    cur_money_list = list()
    cur_money_list.append(money)
    for game in day_dict.values():

        cur_money = cur_money + invest_one_game(game, money) * float(game[2])
        cur_money_list.append(cur_money)

    return cur_money, cur_money_list

def drawK(k_dict):

    k_dict = dict(sorted(k_dict.items()))
    quotes = list()
    for k,v in k_dict.items():
        sdate_num = date2num(datetime.datetime.strptime(k, '%Y-%m-%d'))  # 日期需要特定形式，这里进行转换
        sopen = v[0]
        sclose = v[-1]
        shigh = max(v)
        slow = min(v)
        datas = (sdate_num,sopen,shigh,slow,sclose)
        quotes.append(datas)

    fig, ax = plt.subplots(facecolor=(1, 0.6, 0.6), figsize=(12, 8))
    fig.subplots_adjust(bottom=0.1)
    ax.xaxis_date()
    plt.xticks(rotation=45)  # 日期显示的旋转角度
    plt.title('K')
    plt.xlabel('Time')
    plt.ylabel('Money')
    mpf.candlestick_ohlc(ax, quotes, width=0.7, colorup='r', colordown='green')  # 上涨为红色K线，下跌为绿色，K线宽度为0.7
    plt.grid(True)
    plt.show()
    print("Done.")


def income_count(data_dict, out_dir):

    money = INIT_MONEY
    k_dict = dict()

    for key in data_dict.keys():
        nian_yue_dict = data_dict[key]
        for k in nian_yue_dict.keys():
            day_dict = nian_yue_dict[k]
            money, cur_money_list = invest_one_day(day_dict, money)
            k_dict[k] = cur_money_list
            print("{} : {:.2f} 元".format(k, money))

    # 画k线图
    drawK(k_dict)
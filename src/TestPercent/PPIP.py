'''
    投资方案
'''

import csv
import time
import os

INIT_FUND = 2000

def income_count_fix_percent_each_month(data_dict, out_dir, fix_percent):

    log = out_dir + "/income.log"
    f_log = open(log, "a")
    cur_day_list = []
    cur_day_fund_list = []

    cur_fund = INIT_FUND
    cur_day_fund = INIT_FUND
    cur_running = list()  # [id, num(注数)]
    cur_day = '2019-11-30'
    for key,value in data_dict.items():

        # 判断cur_running中有无比赛结束回收资金
        cur_time = value[0]
        remain_list = list()
        for game in cur_running:
            id = game[0]
            num = game[1]
            game_time = data_dict[id][0]
            if (cur_time - game_time) >= 2.5 * 3600:  # 2.5h比赛已结束
                cur_fund += float(data_dict[id][2]) * num + num # (单注收益 * 注数)
            else:
                remain_list.append(game)
        cur_running = remain_list[:]

        # 当日总结
        if value[1] != cur_day:

            pre_month = cur_day.split("-")[1]
            cur_month = value[1].split("-")[1]

            # print(cur_day + " 结余资金 : {:.2f}".format(cur_fund))
            cur_day = value[1]
            cur_day_list.append(cur_day)
            cur_day_fund_list.append(str(cur_fund))
            if pre_month != cur_month:
                cur_day_fund = INIT_FUND
                cur_fund = INIT_FUND
            else:
                cur_day_fund = cur_fund

        touru =  int(cur_day_fund * fix_percent) # 每日单场比赛投入资金

        # 将当前比赛加入cur_running
        if cur_fund - touru >= 0:
            cur_running.append([key, touru])
            cur_fund -= touru
        # else:
        #     print(key, value)

    # 清空未结算比赛
    for i in range(len(cur_running)):
        id = cur_running[i][0]
        num = cur_running[i][1]
        cur_fund += float(data_dict[id][2]) * num + num  # (单注收益 * 注数)

    # 最终总结
    cur_day_list.append(cur_day)
    cur_day_fund_list.append(str(cur_day_fund))
    print(cur_day + " 结余资金 : {:.2f}".format(cur_fund))

    if os.path.getsize(log) < 2:
        f_log.write("\t".join(cur_day_list))

    f_log.write("\n")
    f_log.write("\t".join(cur_day_fund_list))

    f_log.close()

def income_count_fix_percent_each_week(data_dict, out_dir, fix_percent):

    log = out_dir + "/income.log"
    f_log = open(log, "a")
    cur_day_list = []
    cur_day_fund_list = []

    cur_fund = INIT_FUND
    cur_day_fund = INIT_FUND
    cur_running = list()  # [id, num(注数)]
    cur_day = '2019-11-30'

    for key,value in data_dict.items():

        # 判断cur_running中有无比赛结束回收资金
        cur_time = value[0]
        remain_list = list()
        for game in cur_running:
            id = game[0]
            num = game[1]
            game_time = data_dict[id][0]
            if (cur_time - game_time) >= 2.5 * 3600:  # 2.5h比赛已结束
                cur_fund += float(data_dict[id][2]) * num + num # (单注收益 * 注数)
            else:
                remain_list.append(game)
        cur_running = remain_list[:]

        # 当日总结
        if value[1] != cur_day:

            pre_week = time.strptime(cur_day, "%Y-%m-%d").tm_yday // 7
            cur_week = time.localtime(value[0]).tm_yday // 7

            # print(cur_day + " 结余资金 : {:.2f}".format(cur_fund))
            cur_day = value[1]
            cur_day_list.append(cur_day)
            cur_day_fund_list.append(str(cur_fund))
            if pre_week != cur_week:
                cur_day_fund = INIT_FUND
                cur_fund = INIT_FUND
            else:
                cur_day_fund = cur_fund

        touru =  int(cur_day_fund * fix_percent) # 每日单场比赛投入资金

        # 将当前比赛加入cur_running
        if cur_fund - touru >= 0:
            cur_running.append([key, touru])
            cur_fund -= touru
        # else:
        #     print(key, value)

    # 清空未结算比赛
    for i in range(len(cur_running)):
        id = cur_running[i][0]
        num = cur_running[i][1]
        cur_fund += float(data_dict[id][2]) * num + num  # (单注收益 * 注数)

    # 最终总结
    cur_day_list.append(cur_day)
    cur_day_fund_list.append(str(cur_day_fund))
    print(cur_day + " 结余资金 : {:.2f}".format(cur_fund))

    if os.path.getsize(log) < 2:
        f_log.write("\t".join(cur_day_list))

    f_log.write("\n")
    f_log.write("\t".join(cur_day_fund_list))

    f_log.close()


def income_count(data_dict, out_dir):

    log = out_dir + "/income.log"
    f_log = open(log, "a")
    cur_day_list = []
    cur_day_fund_list = []

    cur_fund = INIT_FUND
    cur_day_fund = INIT_FUND
    cur_running = list()  # [id, num(注数)]
    cur_day = '2019-11-30'
    for key,value in data_dict.items():

        # 判断cur_running中有无比赛结束回收资金
        cur_time = value[0]
        remain_list = list()
        for game in cur_running:
            id = game[0]
            num = game[1]
            game_time = data_dict[id][0]
            if (cur_time - game_time) >= 2.5 * 3600:  # 2.5h比赛已结束
                cur_fund += float(data_dict[id][2]) * num + num # (单注收益 * 注数)
            else:
                remain_list.append(game)
        cur_running = remain_list[:]

        # 当日总结
        if value[1] != cur_day:
            # print(cur_day + " 结余资金 : {:.2f}".format(cur_fund))
            cur_day = value[1]
            cur_day_fund = cur_fund
            cur_day_list.append(cur_day)
            cur_day_fund_list.append(str(cur_day_fund))

        timeArray = time.strptime(value[1], "%Y-%m-%d")
        if timeArray.tm_wday < 5:
            fix_percent = 0.07
        else:
            fix_percent = 0.04
        touru = int(cur_day_fund * fix_percent) # 每日单场比赛投入资金

        # 将当前比赛加入cur_running
        # if cur_fund - touru >= 0:
        if cur_fund - touru >= cur_day_fund * 0.3:
            cur_running.append([key, touru])
            cur_fund -= touru
        # else:
        #     print(key, value)

    # 清空未结算比赛
    for i in range(len(cur_running)):
        id = cur_running[i][0]
        num = cur_running[i][1]
        cur_fund += float(data_dict[id][2]) * num + num  # (单注收益 * 注数)

    # 最终总结
    cur_day_list.append(cur_day)
    cur_day_fund_list.append(str(cur_fund))
    print(cur_day + " 结余资金 : {:.2f}".format(cur_fund))

    if os.path.getsize(log) < 2:
        f_log.write("\t".join(cur_day_list))

    f_log.write("\n")
    f_log.write("\t".join(cur_day_fund_list))

    f_log.close()
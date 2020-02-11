import csv
import time
import os
import src.TestPercent.PPIP as PPIP
import src.TestPercent.ppip_new as ppip

INIT_FUND = 2000

def read_csv(in_csv):
    '''
    读取csv文件，返回data_dict
    :param in_csv:
    :return: data_dict
    '''

    data_dict = dict()
    with open(in_csv, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows[1:]:
            id = row[0]
            time_ = row[5]
            income = row[7]
            state = row[4]
            if state != "3":  # 状态3为正常结束状态
                continue
            bj_time_array = time.strptime(time_, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(bj_time_array)) - 12 * 3600  # 推迟12小时记日期
            football_time_array = time.localtime(timeStamp)
            day = time.strftime("%Y-%m-%d", football_time_array)

            # 去除周末比赛
            # if int(timeArray.tm_wday) >= 5:
            #     continue
            # day = time.strftime("%Y-%m-%d", timeArray)
            
            nian_yue = time.strftime("%Y-%m", bj_time_array)
            if nian_yue not in data_dict:
                data_dict[nian_yue] = dict()
            if day not in data_dict[nian_yue]:
                data_dict[nian_yue][day] = dict()

            data_dict[nian_yue][day][id] = [timeStamp, day, income]

        data_dict = dict(sorted(data_dict.items()))
        for key in data_dict.keys():
            data_dict[key] = dict(sorted(data_dict[key].items()))
            for k in data_dict[key].keys():
                data_dict[key][k] = dict(sorted(data_dict[key][k].items(), key=lambda x:x[1][0]))

    return data_dict

def income_count_fix_percent(data_dict, out_dir, fix_percent):

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

def process(in_csv, out_dir):

    # 1.获取csv文件中的id、时间、盈利
    data_dict = read_csv(in_csv)

    # 这些是旧的
    # 2.投资计算
    # for i in range(20):
    #     fix_percent = 0.01 + i * 0.01
    #     income_count_fix_percent(data_dict, out_dir, fix_percent)
    #     # PPIP.income_count_fix_percent_each_month(data_dict, out_dir, fix_percent)
    #     # PPIP.income_count_fix_percent_each_week(data_dict, out_dir, fix_percent)
    # 3.投资方案
    # PPIP.income_count(data_dict, out_dir)

    # 以下是新的
    ppip.income_count(data_dict, out_dir)

    pass
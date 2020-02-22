'''
    平局情况统计
    统计各大联赛、各个赛季、各个月份的平局率
'''

import time
import csv

weekday_name = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

class Info():

    def __init__(self):

        self.game_id = None
        self.year = None
        self.month = None
        self.day = None
        self.weekday = None
        self.league_id = None
        self.is_draw = None
        self.bet365_draw_odd = None

    def print(self):
        print(vars(self))

class DrawInfo(Info):

    def __init__(self, line_list):
        super().__init__()
        self._pares_info_(line_list)

    def _pares_info_(self, line_list):

        self.game_id = int(line_list[0])
        if int(line_list[1]) == int(line_list[2]):
            self.is_draw = True
        else:
            self.is_draw = False
        time_info = time.localtime(int(line_list[3]) // 1000)
        self.year = time_info.tm_year
        self.month = time_info.tm_mon
        self.day = time_info.tm_mday
        self.weekday = weekday_name[time_info.tm_wday]
        self.league_id = int(line_list[4])
        self.bet365_draw_odd = float(line_list[9])

class DrawInfo2(Info):

    def __init__(self, line_list):
        super().__init__()
        self._pares_info_(line_list)

    def _pares_info_(self, line_list):

        self.game_id = int(line_list[8])
        if float(line_list[7]) > 0:
            self.is_draw = True
        else:
            self.is_draw = False
        time_str = line_list[9]
        time_info = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        self.year = time_info.tm_year
        self.month = time_info.tm_mon
        self.day = time_info.tm_mday
        self.weekday = weekday_name[time_info.tm_wday]
        self.league_id = int(line_list[10])
        self.bet365_draw_odd = float(line_list[24])

class StaticHandler():

    def __init__(self):
        self.full_dict = dict()

    def enter_draw_info(self, draw_info):
        '''
        运行统计
        :param draw_info: DrawInfo的实体
        :return: null
        '''

        if draw_info.league_id not in self.full_dict:
            self.full_dict[draw_info.league_id] = dict()

        if draw_info.weekday in ['mon', 'tue', 'wed', 'thu']:
            if draw_info.month < 10:
                key = "{}-0{}-{}".format(draw_info.year, draw_info.month, "O")
            else:
                key = "{}-{}-{}".format(draw_info.year, draw_info.month, "O")
        else:
            if draw_info.month < 10:
                key = "{}-0{}-{}".format(draw_info.year, draw_info.month, "weekend")
            else:
                key = "{}-{}-{}".format(draw_info.year, draw_info.month, "weekend")

        if key not in self.full_dict[draw_info.league_id]:
            self.full_dict[draw_info.league_id][key] = [0, 0, 0.0]

        self.full_dict[draw_info.league_id][key][1] += 1
        if draw_info.is_draw:
            self.full_dict[draw_info.league_id][key][0] += 1

    def get_rate(self):
        '''
        计算平局占有率
        :return: null
        '''
        for v in self.full_dict.values():
            for vv in v.values():
                if vv[1] != 0:
                    vv[2] = float(vv[0]) / vv[1]

    def print(self, out_path, league_name_dict):

        with open(out_path, "w") as f:
            league_ids = [league_id for league_id in self.full_dict.keys()]
            league_ids = sorted(league_ids)
            league_names = list()
            for id in league_ids:
                league_names.append(league_name_dict[id])

            f.write("league_ids\t" + "\t".join(league_names) + "\ttotal\n")
            month_ids = [month_id for month_id in self.full_dict[1].keys()]
            month_ids = sorted(month_ids)
            for month_id in month_ids:
                f.write(month_id + "\t")
                month_total = 0
                month_num = 0
                for league_id in league_ids:
                    league_dict = self.full_dict[int(league_id)]
                    if month_id in league_dict:
                        month_total += league_dict[month_id][1]
                        month_num += league_dict[month_id][0]
                        f.write("{}场-{:.2f} %\t".format(league_dict[month_id][1], league_dict[month_id][2]*100))
                    else:
                        f.write("{}场-{:.2f} %\t".format(0, 0.0))
                if month_total > 0:
                    month_rate = float(month_num) / month_total
                else:
                    month_rate = 0.0
                f.write("{}场-{:.2f} %\n".format(month_total, month_rate*100))

            weekday_total = 0
            weekday_num = 0
            f.write("O\t")
            for league_id in league_ids:
                league_total = 0
                league_num = 0
                league_dict = self.full_dict[int(league_id)]
                for month_id in month_ids:
                    if month_id.find("-O") < 0:
                        continue
                    if month_id in league_dict:
                        league_total += league_dict[month_id][1]
                        league_num += league_dict[month_id][0]
                if league_total > 0:
                    league_rate = float(league_num) / league_total
                else:
                    league_rate = 0.0

                f.write("{}场-{:.2f} %\t".format(league_total, league_rate*100))
                weekday_total += league_total
                weekday_num += league_num
            weekday_rate = float(weekday_num) / weekday_total
            f.write("{}场-{:.2f} %\n".format(weekday_total, weekday_rate*100))

            weekend_total = 0
            weekend_num = 0
            f.write("weekend\t")
            for league_id in league_ids:
                league_total = 0
                league_num = 0
                league_dict = self.full_dict[int(league_id)]
                for month_id in month_ids:
                    if month_id.find("-weekend") < 0:
                        continue
                    if month_id in league_dict:
                        league_total += league_dict[month_id][1]
                        league_num += league_dict[month_id][0]
                if league_total > 0:
                    league_rate = float(league_num) / league_total
                else:
                    league_rate = 0.0

                f.write("{}场-{:.2f} %\t".format(league_total, league_rate*100))
                weekend_total += league_total
                weekend_num += league_num
            weekend_rate = float(weekend_num) / weekend_total
            f.write("{}场-{:.2f} %\n".format(weekend_total, weekend_rate*100))

            all_total = 0
            all_num = 0
            f.write("total\t")
            for league_id in league_ids:
                league_total = 0
                league_num = 0
                league_dict = self.full_dict[int(league_id)]
                for month_id in month_ids:
                    if month_id in league_dict:
                        league_total += league_dict[month_id][1]
                        league_num += league_dict[month_id][0]
                if league_total > 0:
                    league_rate = float(league_num) / league_total
                else:
                    league_rate = 0.0

                f.write("{}场-{:.2f} %\t".format(league_total, league_rate*100))
                all_total += league_total
                all_num += league_num
            all_rate = float(all_num) / all_total
            f.write("{}场-{:.2f} %".format(all_total, all_rate*100))

def load_league_name(csv_path):

    league_dict = dict()
    with open(csv_path) as f:

        reader = csv.reader(f)
        rows = list(reader)
        for row in rows[1:]:
            league_id = int(row[0])
            league_name = row[2]
            league_dict[league_id] = league_name
    return league_dict

def run(datas, out_path, type=0):  # 数据list type==0表示赛前数据、type==1表示平局预测数据

    league_dict = load_league_name("/Users/user/Github/income-test/data/league.csv")

    static_handler = StaticHandler()
    for data in datas:
        if type == 0:
            draw_info = DrawInfo(data)
        elif type == 1:
            draw_info = DrawInfo2(data)
        static_handler.enter_draw_info(draw_info)

    static_handler.get_rate()
    static_handler.print(out_path, league_dict)

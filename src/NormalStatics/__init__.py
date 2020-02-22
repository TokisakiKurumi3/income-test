'''
    本模块用于一般性赛前统计(需要提供含有联赛id的数据)
'''

import os
import logging
from src.NormalStatics import DrawStatics as ds
import csv

logging.getLogger().setLevel(logging.DEBUG)

def read_csv(in_csv):

    with open(in_csv, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        return rows[1:]

def read_data(data_path):
    '''
    读取数据文本路径
    :return: 数据list
    '''
    data = list()

    if not os.path.exists(data_path):
        logging.warning("no data path = {}".format(data_path))

    with open(data_path) as f:

        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            data.append(line)

    return data

def main():

    data_dir = "/Users/user/PycharmProjects/with_model/data/"

    data = list()
    data += read_data(data_dir + "/test1.txt")
    data += read_data(data_dir + "/test2.txt")

    out_path = "/Users/user/Desktop/tmp/result.txt"

    ds.run(data, out_path)

    # predict_draw_data = "/Users/user/Github/income-test/data/460.csv"
    # out_path = "/Users/user/Desktop/tmp/result2.txt"
    # csv_data = read_csv(predict_draw_data)
    # ds.run(csv_data, out_path, type=1)

if __name__ == '__main__':
    main()
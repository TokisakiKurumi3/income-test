'''
    用于评测此单场比赛投资百分比
'''

import sys
import logging
import src.TestPercent.processor as processor

def run():

    if not len(sys.argv) == 3:
        logging.error("Usage: __init__.py in.csv out_dir")
        exit(1)

    in_csv = sys.argv[1]
    out_dir = sys.argv[2]

    processor.process(in_csv, out_dir)

    pass

def main():

    run()

    pass

if __name__ == '__main__':
    main()
# -*- coding:utf-8 -*-
import sys
from util import logUtil
from   dao  import dao_comp_weekly_commons as  compCommDao
from   dao  import dao_comp_weekly_qfq as  compQfqDao
import sys
from pathlib import Path
import time
sys.path.append(str(Path(__file__).resolve().parents[1]))  # 将父级目录加入执行目录列表
import runner_compute.runner_com_indexs  as idx
"""
采集日数据
"""
class RunnerWeeklyCompCommons( ):

    def __init__(self ):
        self.logger = logUtil.Logger('stockstore')





    # 对复权因子发生变化的重新计算
    def reCompQfqByDate(self, trade_date):
        # print("前复权计算")
        start_time = time.time()
        self.logger.info(  "计算周线潜伏期数据开始")
        compQfqDao.reCompQfqByDate(trade_date)
        stop_time = time.time()
        self.logger.info(  "计算周线前复权数据结束，耗时："+f'{stop_time - start_time:.4f}s')



    def runCompWeeklyCommonsByDate(self,trade_date):

        start_time = time.time()
        self.logger.info(  "采集周线数据开始")
        compCommDao.runCompWeeklyCommonsByDate(trade_date)
        stop_time = time.time()
        self.logger.info(  "采集周线数据结束，耗时："+f'{stop_time - start_time:.4f}s')

    def runCompWeeklyCommonsByStock(self,ts_code):
        compCommDao.runByCode(ts_code)
 
# -*- coding:utf-8 -*-
import time

from   dao  import dao_spider_trade_cal as  daoCal
from   dao  import dao_spider_trade_cal as  daoCal
from runner_spider.runner_stock_basic import RunerStockBasic
from runner_spider.runner_spider_daily import    RunnerSpiderDaily
from runner_spider.runner_spider_weekly import    RunnerSpiderWeekly
from runner_spider.runner_spider_adjfactor import    RunnerSpiderAdjfactor
from runner_spider.runner_spider_dailybasic import    RunnerSpiderDailyBasic
from runner_compute.runner_comp_daily_commons import    RunnerDailyCompCommons
from runner_compute.runner_comp_weekly_commons import    RunnerWeeklyCompCommons
from runner_copy.runner_copy import    RunnerCopy
from util import logUtil
"""
定时任务运行器
"""
class RunnerSpiderRunner( ):

    def __init__(self ,runner):
        self.logger = logUtil.Logger('stockstore')
        self.logger.info(  "自动采集计算启动")

    def start_runner(self):
        df = daoCal.DaoQueryCalDateByLast4AnyTradeDate()
        for  index,row in df.iterrows()  :
             self.spider_runner(row['cal_date'])

    def spider_runner(self,date):
            self.logger.info( "自动采集执行...")
            if (date == None ):
                date = time.strftime("%Y-%m-%d", time.localtime())
            df = daoCal.DaoQueryCalDateByLastTradeDate(date)
            if ( df.empty or  len(df)<1 ) : 
                self.logger.info(  "查询没有可采集的计划")
                return
            if (df["stock_basic_spider"][0] != 1):
                self.logger.info(  "1、采集基本信息")
                RunerStockBasic().run(str(date).replace('-', ''))

            if (df["daily_spider"][0] != 1):
                self.logger.info(  "2、采集日线数据")
                RunnerSpiderDaily().runByDate(str(date).replace('-', ''))

            if (df["adj_factor_spider"][0] != 1):
                self.logger.info(  "3、采集复权因子")
                RunnerSpiderAdjfactor().runByDate(str(date).replace('-', ''),df["daily_spider"][0])
                
            if (df["daily_spider"][0] != 1):
                self.logger.info(  "4、计算前复权日线数据")
                RunnerDailyCompCommons().reCompQfqByDate(str(date).replace('-', ''))

            if (df["daily_basic_spider"][0] != 1):
                self.logger.info(  "5、采集每日指标")
                RunnerSpiderDailyBasic().runByDate(str(date))

            df = daoCal.DaoQueryCalDateByTradeDate(date)
            if (df["daily_compute"][0] != 1 and df["adj_factor_spider"][0] == 1 and df["daily_spider"][0] == 1):
                self.logger.info(  "6、计算日线指标")
                RunnerDailyCompCommons().runCompDailyCommonsByDate(str(date).replace('-', ''))


            df = daoCal.DaoQueryCalDateByTradeDate(date)
            if (df["weekly_spider"][0] != 1  ):
                self.logger.info( "7、采集周线数据")
                RunnerSpiderWeekly().runByDate(str(date).replace('-', ''))


            if (df["weekly_spider"][0] != 1):
                self.logger.info(  "8、计算前复权周线数据")
                RunnerWeeklyCompCommons().reCompQfqByDate(str(date).replace('-', ''))

            df = daoCal.DaoQueryCalDateByTradeDate(date)
            if (df["weekly_compute"][0] != 1 and df["adj_factor_spider"][0] == 1 and df["weekly_spider"][0] == 1 ):
                self.logger.info( "9、计算周线指标")
                RunnerWeeklyCompCommons().runCompWeeklyCommonsByDate(str(date))


            df = daoCal.DaoQueryCalDateByTradeDate(date)
            if (df["daily_compute"][0] == 1  and df["daily_spider"][0] == 1):
                self.logger.info( "10、拷贝数据")
                RunnerCopy("准备拷贝数据").runCopyByDate(date)

   

if __name__ == '__main__':
    pass





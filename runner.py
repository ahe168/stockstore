# -*- coding:utf-8 -*- 
from util import logUtil
from apscheduler.schedulers.blocking import BlockingScheduler
from runner_spider import RunnerSpiderRunner
from config.config_cron import ConfigCron
"""
定时任务
"""
class Runner( ):

    def __init__(self,runner ):
        self.logger = logUtil.Logger('stockstore')
        self.logger.info(runner)


    def initCron(self):
        self.executor = None
        self.db = ConfigCron()

        self.data = self.db.config_db_read()
        scheduler = BlockingScheduler(timezone='Asia/Shanghai')
        scheduler.add_job(RunnerSpiderRunner("").start_runner, 'cron', month=str( self.data[0]["monthly"]), day=str( self.data[0]["daily"]), hour=str( self.data[0]["house"]), minute=str( self.data[0]["minute"]), second=str( self.data[0]["second"]))
        try:
            scheduler.start()
        except SystemExit as e:
            self.logger.error(e)


if __name__ == '__main__':
    Runner('' ).initCron()
    RunnerSpiderRunner("").start_runner()


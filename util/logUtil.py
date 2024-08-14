import logging
import os
import time
from logging.handlers import  RotatingFileHandler


class Logger():


    def __init__(self, name):
        logs_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/output/logs' 
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
    

        self.logger = logging.getLogger(name)

		#设置级别，只有等于或高于设置的级别才会写入到文件中
        self.logger.setLevel(logging.INFO)

        #定义日志输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 创建一个handler，用于写入日志文件，按照日志大小自动切换
        timestamp = time.strftime('%Y%m%d')
        rotating_handler = RotatingFileHandler(
            filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/output/logs', "{}.log".format(timestamp)),
            maxBytes=100 *1024 * 1024,
            encoding='utf-8')
        rotating_handler.setFormatter(formatter)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(rotating_handler)
        self.logger.addHandler(ch)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


# 使用Logger类
if __name__ == '__main__':
    logger = Logger('login')
    logger.info('This is  info message')
    logger.debug('This idebug message')
    logger.warning('This i warning message')
    logger.error('This is error message')
    logger.critical('This is critical message')



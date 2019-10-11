import logging

## 输出日志    handler 句柄
logging_hander = logging.FileHandler("test.log",encoding="utf8")
stream_hander = logging.StreamHandler()
log_format = "%(asctime)s【%(levelname)s】%(message)s"    ## 日志格式
## 时间格式
time_format = "%Y-%m-%d %H:%M:%S"
## 日志配置
## 设置日志等级
logging.basicConfig(level=logging.DEBUG,format=log_format,datefmt=time_format,handlers=[logging_hander,stream_hander])
### 调试   最详细的日志等级，通常用于问题  项目的调试过程
logging.debug("这是debug等级")
### 详细程度仅次于debug 记录通常是关键节点的信息
logging.info("这是info等级")
### 警告 当某些不被期望的错误发生，但是不影响程序运行
logging.warning("这是warning等级")
### 出现严重的问题，导致部分功能不能运行
logging.error("这是error等级")
## 严重错误，导致程序中断
logging.critical("这是critical等级")
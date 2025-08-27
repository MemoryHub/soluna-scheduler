import time
import signal
import sys
from logging_config import global_logger as logger
from scheduler import soluna_scheduler

def signal_handler(sig, frame):
    """处理终止信号"""
    logger.info("接收到终止信号，准备关闭程序...")
    soluna_scheduler.shutdown()
    logger.info("程序已安全关闭")
    sys.exit(0)

def main():
    """主程序入口"""
    try:
        # 注册信号处理器
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("Soluna定时任务调度器启动中...")
        
        # 启动调度器
        soluna_scheduler.start()
        
        # 保持程序运行
        logger.info("Soluna定时任务调度器已成功启动。按Ctrl+C退出。")
        while True:
            time.sleep(60)  # 每分钟检查一次
            
    except Exception as e:
        logger.error(f"程序运行异常: {str(e)}")
        soluna_scheduler.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main()
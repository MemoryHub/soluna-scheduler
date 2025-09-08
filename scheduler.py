import os
import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from logging_config import global_logger as logger
from api_client import soluna_api_client

# 加载环境变量
load_dotenv()

class SolunaScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.cron_expression = os.getenv('SCHEDULER_CRON_EXPRESSION', '0 0 * * *')  # 默认每天凌晨0点执行
        
    def start(self):
        """启动调度器"""
        # 添加每日生活轨迹生成任务
        self.scheduler.add_job(
            func=self.generate_daily_life_paths,
            trigger=CronTrigger.from_crontab(self.cron_expression),
            id='daily_life_path_generation',
            name='每天生成所有角色的生活轨迹',
            replace_existing=True
        )
        
        # 添加30分钟情绪更新任务
        self.scheduler.add_job(
            func=self.update_emotions_every_thirty_minutes,
            trigger=CronTrigger.from_crontab('*/30 * * * *'),  # 每30分钟执行一次
            id='thirty_minutes_emotion_update',
            name='每30分钟更新所有角色情绪',
            replace_existing=True
        )
        
        # 启动调度器
        self.scheduler.start()
        logger.info(f"调度器已启动，定时任务配置: {self.cron_expression}, 30分钟情绪更新已启用")
        
    def shutdown(self):
        """关闭调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("调度器已关闭")
            
    def generate_daily_life_paths(self):
        """生成当天所有角色的生活轨迹"""
        try:
            logger.info("开始执行每日批量生成生活轨迹任务")
            
            # 获取当天的日期
            today = datetime.date.today()
            today_str = today.strftime('%Y-%m-%d')
            
            # 调用API生成生活轨迹
            result = soluna_api_client.batch_generate_life_paths(
                start_date=today_str,
                end_date=today_str,
                max_events=3,
                limit=0  # 处理所有角色
            )
            
            # 记录任务完成信息
            if result:
                # 无论部分角色是否失败，只要API返回200，都认为任务成功执行
                success_count = result.get('data', {}).get('success_count', 0)
                failed_count = result.get('data', {}).get('failed_count', 0)
                logger.info(f"每日批量生成生活轨迹任务完成，成功: {success_count}个，失败: {failed_count}个")
            
        except Exception as e:
            logger.error(f"每日批量生成生活轨迹任务执行失败: {str(e)}")
            # 这里可以添加告警通知逻辑，例如发送邮件、消息等
            
    def update_emotions_every_thirty_minutes(self):
        """每30分钟更新所有角色情绪"""
        try:
            logger.info("开始执行30分钟情绪更新任务")
            
            # 调用API更新最近30分钟的情绪
            result = soluna_api_client.update_emotions_from_recent_events()
            
            # 记录任务完成信息
            if result:
                updated_count = result.get('data', {}).get('updated_count', 0)
                total_count = result.get('data', {}).get('total_count', 0)
                logger.info(f"30分钟情绪更新任务完成，成功更新: {updated_count}个角色，总计: {total_count}个角色")
            
        except Exception as e:
            logger.error(f"30分钟情绪更新任务执行失败: {str(e)}")
            # 这里可以添加告警通知逻辑，例如发送邮件、消息等

# 创建调度器实例供主程序使用
soluna_scheduler = SolunaScheduler()

# 主程序入口
if __name__ == "__main__":
    try:
        logger.info("启动Soluna调度器...")
        soluna_scheduler.start()
        
        # 保持程序运行
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭调度器...")
        soluna_scheduler.shutdown()
        logger.info("调度器已正常退出")
    except Exception as e:
        logger.error(f"调度器启动失败: {str(e)}")
        raise
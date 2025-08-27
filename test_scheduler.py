import os
import datetime
import time
from dotenv import load_dotenv
from logging_config import global_logger as logger
from api_client import SolunaApiClient

# 加载环境变量
load_dotenv()

# 临时修改环境变量用于测试
os.environ['LOG_LEVEL'] = 'DEBUG'

def test_api_client():
    """测试API客户端"""
    logger.info("开始测试API客户端...")
    
    client = SolunaApiClient()
    
    # 测试用日期（使用今天的日期）
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')
    
    try:
        # 使用limit=3来限制只处理3个角色，加快测试速度
        result = client.batch_generate_life_paths(
            start_date=today_str,
            end_date=today_str,
            max_events=1,
            limit=0
        )
        
        logger.info(f"API调用测试结果: {result}")
        return True
    except Exception as e:
        logger.error(f"API调用测试失败: {str(e)}")
        return False

def test_scheduler_logic():
    """测试调度器逻辑"""
    logger.info("开始测试调度器逻辑...")
    
    # 模拟调度器的任务执行逻辑
    try:
        today = datetime.date.today()
        today_str = today.strftime('%Y-%m-%d')
        
        logger.info(f"模拟生成{today_str}的生活轨迹")
        
        # 这里可以根据需要添加更多的测试逻辑
        
        return True
    except Exception as e:
        logger.error(f"调度器逻辑测试失败: {str(e)}")
        return False

def main():
    """测试主函数"""
    logger.info("Soluna Scheduler测试程序启动")
    
    # 测试API客户端
    api_test_result = test_api_client()
    
    # 测试调度器逻辑
    scheduler_test_result = test_scheduler_logic()
    
    # 输出测试结果
    if api_test_result and scheduler_test_result:
        logger.info("所有测试通过！")
        return 0
    else:
        logger.error("部分测试失败，请检查日志！")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
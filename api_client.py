import os
import time
import requests
from dotenv import load_dotenv
from logging_config import global_logger as logger

# 加载环境变量
load_dotenv()

class SolunaApiClient:
    def __init__(self):
        self.api_url = os.getenv('SOLUNA_API_URL', 'http://localhost:8000')
        self.batch_generate_endpoint = os.getenv('SOLUNA_BATCH_GENERATE_ENDPOINT', '/api/life-paths/batch-generate-all')
        self.emotion_update_endpoint = os.getenv('SOLUNA_EMOTION_UPDATE_ENDPOINT', '/api/emotion/characters/update/thirty-minutes')
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.retry_delay = int(os.getenv('RETRY_DELAY', '30'))
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '300'))
        
        # 构建完整的API URL
        self.full_batch_generate_url = f"{self.api_url}{self.batch_generate_endpoint}"
        self.full_emotion_update_url = f"{self.api_url}{self.emotion_update_endpoint}"
        
    def batch_generate_life_paths(self, start_date, end_date, max_events=3, limit=0):
        """
        调用批量生成生活轨迹API
        
        Args:
            start_date: 开始日期 (格式: YYYY-MM-DD)
            end_date: 结束日期 (格式: YYYY-MM-DD)
            max_events: 每个角色生成的最大事件数
            limit: 限制处理的角色数量，0表示不限制
            
        Returns:
            dict: API响应结果
        """
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "max_events": max_events,
            "limit": limit
        }
        
        retries = 0
        while retries <= self.max_retries:
            try:
                logger.info(f"调用批量生成生活轨迹API，参数: {data}")
                
                # 发送POST请求
                response = requests.post(
                    self.full_batch_generate_url,
                    json=data,
                    timeout=self.timeout
                )
                
                # 检查响应状态
                response.raise_for_status()
                
                # 解析响应结果
                result = response.json()
                
                # 只要HTTP状态码为200就认为成功
                logger.info(f"批量生成生活轨迹API调用成功，结果: {result}")
                return result
            except requests.exceptions.RequestException as e:
                logger.error(f"批量生成生活轨迹API调用异常: {str(e)}")
                
                # 如果是最后一次重试，则抛出异常
                if retries == self.max_retries:
                    raise e
            
            # 重试前等待
            retries += 1
            logger.info(f"第{retries}次重试，等待{self.retry_delay}秒...")
            time.sleep(self.retry_delay)
                
    def update_emotions_from_recent_events(self):
        """
        调用30分钟情绪更新API
        
        Returns:
            dict: API响应结果
        """
        retries = 0
        while retries <= self.max_retries:
            try:
                logger.info("调用30分钟情绪更新API")
                
                # 发送POST请求
                response = requests.post(
                    self.full_emotion_update_url,
                    json={},
                    timeout=self.timeout
                )
                
                # 检查响应状态
                response.raise_for_status()
                
                # 解析响应结果
                result = response.json()
                
                logger.info(f"30分钟情绪更新API调用成功，结果: {result}")
                return result
                
            except requests.exceptions.RequestException as e:
                logger.error(f"30分钟情绪更新API调用异常: {str(e)}")
                
                # 如果是最后一次重试，则抛出异常
                if retries == self.max_retries:
                    raise e
                    
            # 重试前等待
            retries += 1
            logger.info(f"第{retries}次重试，等待{self.retry_delay}秒...")
            time.sleep(self.retry_delay)

# 创建API客户端实例供其他模块使用
soluna_api_client = SolunaApiClient()
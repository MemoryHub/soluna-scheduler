# Soluna Scheduler

一个用于管理Soluna项目定时任务的Python服务。

## 功能特性

- 🕒 **定时任务调度**：每天凌晨0点自动执行批量生成生活轨迹任务
- ⚙️ **可配置的执行时间**：通过环境变量灵活设置Cron表达式
- 🔄 **自动重试机制**：API调用失败时支持自动重试
- 📊 **完善的日志记录**：详细记录任务执行情况、API调用结果和异常信息
- 🔒 **环境变量配置**：敏感信息和配置项通过环境变量管理

## 项目结构

```
soluna-scheduler/
├── requirements.txt     # 项目依赖
├── .env                 # 环境变量配置
├── .gitignore           # Git忽略文件
├── logging_config.py    # 日志配置
├── api_client.py        # Soluna API客户端
├── scheduler.py         # 定时任务调度器
├── main.py              # 主程序入口
└── README.md            # 项目说明文档
```

## 安装与配置

1. **克隆项目**

```bash
git clone <项目地址>
cd soluna-scheduler
```

2. **创建虚拟环境并安装依赖**

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

3. **配置环境变量**

复制并编辑.env文件，根据实际情况修改配置：

```bash
# Soluna API配置
SOLUNA_API_URL=http://localhost:8000
SOLUNA_BATCH_GENERATE_ENDPOINT=/api/event/life-path/batch-generate-all

# 定时任务配置
SCHEDULER_CRON_EXPRESSION=0 0 * * *  # 每天凌晨0点执行

# 重试配置
MAX_RETRIES=3
RETRY_DELAY=30  # 秒

# 请求超时配置
REQUEST_TIMEOUT=300  # 秒

# 日志配置
LOG_LEVEL=INFO
```

## 使用方法

1. **启动服务**

```bash
python main.py
```

2. **查看日志**

日志会同时输出到控制台和scheduler.log文件中，可通过以下命令查看：

```bash
tail -f scheduler.log
```

## 开发说明

- 如需修改定时任务执行逻辑，请编辑`scheduler.py`文件
- 如需调整API调用参数，请修改`api_client.py`文件
- 所有配置项应通过`.env`文件进行设置，避免硬编码

## 异常处理

- 服务支持优雅关闭，接收到SIGINT（Ctrl+C）或SIGTERM信号时会自动关闭调度器
- API调用失败时会根据配置自动重试，达到最大重试次数后记录错误日志
- 所有异常都会被捕获并记录到日志中，确保服务不会意外崩溃

## 监控与告警

当前版本已实现详细的日志记录，可通过日志监控任务执行情况。如需集成更高级的告警系统（如邮件、Slack等），可在`scheduler.py`中的异常处理部分添加相应逻辑。
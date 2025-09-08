# Soluna Scheduler - 智能角色事件调度系统

Soluna Scheduler是Soluna生态系统的核心调度组件，负责定时生成角色事件、维护生活轨迹、管理数据同步和系统监控。作为整个系统的"时间引擎"，它确保角色世界能够持续运转，为用户提供丰富、连贯的角色体验。

## 🎯 系统定位

Soluna Scheduler作为Soluna生态系统的"心跳"，承担着以下关键职责：
- **事件调度引擎**: 定时为角色生成日常和关键事件
- **数据维护**: 清理过期数据、优化存储结构
- **系统监控**: 监控系统健康状态、生成运行报告
- **任务协调**: 协调后端API与前端应用的同步

## 🏗️ 技术架构

- **调度框架**: APScheduler (Python)
- **数据库**: MySQL + MongoDB
- **API通信**: HTTP REST API
- **日志系统**: 结构化日志 + 文件轮转
- **监控**: 自定义监控指标
- **部署**: Docker容器化

## ✨ 核心功能

### ⏰ 事件调度系统
- **定时事件生成**: 每30分钟为活跃角色生成日常事件
- **关键事件调度**: 根据角色状态触发重要人生节点
- **批量处理**: 高效处理大量角色的并发事件生成
- **失败重试**: 智能重试机制处理网络异常
- **优先级队列**: 重要角色优先处理

### 🧹 数据维护系统
- **过期数据清理**: 自动清理过期的事件和临时数据
- **数据库优化**: 定期重建索引、压缩数据
- **备份同步**: 关键数据的增量备份
- **日志轮转**: 自动管理日志文件大小和保留期
- **性能监控**: 数据库性能指标收集

### 📊 系统监控
- **健康检查**: 定期检查系统各组件状态
- **性能指标**: 收集调度任务执行时间、成功率等
- **异常告警**: 任务失败、系统异常时发送通知
- **运行报告**: 生成每日/周/月的系统运行报告
- **资源监控**: CPU、内存、磁盘使用情况监控

### 🔄 数据同步
- **API状态同步**: 与后端API保持状态同步
- **缓存更新**: 更新Redis缓存中的热点数据
- **数据一致性**: 确保MySQL和MongoDB数据一致
- **批量操作**: 高效的批量数据更新

## 📁 项目结构

```
soluna-scheduler/
├── main.py                 # 主调度程序入口
├── scheduler.py           # 核心调度器类
├── api_client.py          # API客户端模块
├── logging_config.py      # 日志配置
├── requirements.txt       # Python依赖
├── start_scheduler.sh     # 启动脚本
├── test_scheduler.py      # 测试脚本
├── .gitignore            # Git忽略文件
├── __pycache__/          # Python缓存目录
└── README.md             # 项目文档
```

## 🔧 配置文件说明

### 环境变量配置
```bash
# 数据库配置
DATABASE_URL=mysql://user:password@localhost/soluna
MONGODB_URL=mongodb://localhost:27017/soluna

# API配置
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30

# 调度配置
SCHEDULE_INTERVAL_MINUTES=30
BATCH_SIZE=50
MAX_RETRIES=3

# 监控配置
ENABLE_MONITORING=true
ALERT_WEBHOOK_URL=https://hooks.slack.com/services/...

# 日志配置
LOG_LEVEL=INFO
LOG_FILE_PATH=/var/log/soluna-scheduler/
MAX_LOG_FILE_SIZE=10MB
LOG_BACKUP_COUNT=5
```

## 🚀 快速开始

### 1. 环境准备
```bash
# 安装Python 3.8+
python --version

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量
创建 `.env` 文件并配置相关参数：

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置文件
vim .env
```

### 3. 启动调度器
```bash
# 开发模式
python main.py

# 生产模式（后台运行）
nohup python main.py > scheduler.log 2>&1 &

# 使用启动脚本
./start_scheduler.sh
```

### 4. Docker部署
```bash
# 构建镜像
docker build -t soluna-scheduler .

# 运行容器
docker run -d \
  --name soluna-scheduler \
  --restart unless-stopped \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/logs:/app/logs \
  soluna-scheduler
```

## 📊 调度任务详解

### 事件生成任务
**任务名称**: `generate_character_events`
- **执行频率**: 每天凌晨0点
- **处理逻辑**:
  1. 获取所有角色列表
  2. 为每个角色生成当天的生活轨迹
  3. 调用API生成个性化事件
  4. 记录生成结果和异常
- **失败处理**: 失败后重试3次，记录到错误日志

### 情绪更新任务
**任务名称**: `update_emotions_every_thirty_minutes`
- **执行频率**: 每30分钟
- **处理逻辑**:
  1. 获取所有角色最近30分钟的生活轨迹
  2. 基于PAD三维度数值计算情绪变化
  3. 批量更新MySQL emotions表中的情绪数值
  4. 记录更新统计信息
- **失败处理**: 失败后重试3次，记录到错误日志

### 数据清理任务
**任务名称**: `cleanup_expired_data`
- **执行频率**: 每天凌晨2点
- **清理内容**:
  - 过期的事件数据（30天前）
  - 未使用的临时文件
  - 过期的用户会话
  - 系统日志归档

### 系统监控任务
**任务名称**: `system_health_check`
- **执行频率**: 每5分钟
- **监控指标**:
  - 数据库连接状态
  - API服务可用性
  - 磁盘空间使用率
  - 内存和CPU使用率
  - 任务队列长度

### 性能优化任务
**任务名称**: `optimize_database`
- **执行频率**: 每天凌晨3点
- **优化内容**:
  - 重建数据库索引
  - 更新统计信息
  - 压缩数据文件
  - 清理碎片

## 🔍 监控和日志

### 日志结构
```
logs/
├── scheduler.log          # 主调度日志
├── events.log            # 事件生成日志
├── errors.log            # 错误日志
├── performance.log       # 性能日志
└── health_check.log      # 健康检查日志
```

### 监控指标
- **任务成功率**: 成功完成的任务百分比
- **平均执行时间**: 各类任务的平均耗时
- **错误率**: 任务失败的频率
- **系统负载**: CPU、内存、磁盘使用情况
- **数据库性能**: 查询响应时间、连接数

### 告警机制
- **邮件通知**: 任务失败、系统异常
- **Slack通知**: 实时告警推送
- **短信通知**: 关键故障紧急通知
- **Web界面**: 可视化监控面板

## 🧪 测试

### 单元测试
```bash
# 运行所有测试
python test_scheduler.py

# 运行特定测试
python -m pytest tests/test_scheduler.py::test_event_generation
```

### 集成测试
```bash
# 测试API连接
python -c "from api_client import APIClient; print(APIClient().test_connection())"

# 测试数据库连接
python -c "from scheduler import Scheduler; Scheduler().test_db_connection()"
```

### 性能测试
```bash
# 压力测试
python scripts/load_test.py --characters 1000 --duration 3600

# 内存使用测试
python scripts/memory_test.py --interval 60
```

## 🛠️ 故障排除

### 常见问题

#### 1. 任务执行失败
```bash
# 检查日志
tail -f logs/errors.log

# 验证API连接
curl -X POST http://localhost:8000/api/health
```

#### 2. 数据库连接问题
```bash
# 检查数据库状态
mysql -u root -p -e "SELECT 1"
mongosh --eval "db.runCommand('ping')"

# 检查连接配置
python -c "import os; print(os.getenv('DATABASE_URL'))"
```

#### 3. 内存泄漏
```bash
# 监控内存使用
ps aux | grep python

# 检查日志轮转
ls -la logs/
```

### 调试工具
```python
# 启用调试模式
export DEBUG=true

# 手动触发任务
python -c "from scheduler import Scheduler; Scheduler().run_event_generation()"

# 查看任务状态
python -c "from scheduler import Scheduler; print(Scheduler().get_task_status())"
```

## 🔮 扩展功能

### 自定义调度器
```python
from scheduler import Scheduler

# 创建自定义调度器
class CustomScheduler(Scheduler):
    def custom_task(self):
        # 自定义任务逻辑
        pass

# 注册自定义任务
scheduler = CustomScheduler()
scheduler.add_job(
    func=scheduler.custom_task,
    trigger='interval',
    minutes=60,
    id='custom_task'
)
```

### 插件系统
```python
# 创建插件目录
mkdir plugins/

# 示例插件结构
plugins/
├── __init__.py
├── weather_plugin.py      # 天气事件插件
├── social_plugin.py       # 社交事件插件
└── economic_plugin.py     # 经济事件插件
```

### API扩展
```python
# 扩展API客户端
class ExtendedAPIClient:
    def get_weather_events(self, location):
        # 获取天气相关事件
        pass
    
    def get_social_trends(self):
        # 获取社交趋势
        pass
```

## 📈 性能优化

### 数据库优化
- **连接池**: 使用连接池管理数据库连接
- **索引优化**: 为常用查询字段添加索引
- **批量操作**: 使用批量插入/更新减少数据库往返
- **缓存策略**: 缓存热点数据减少数据库压力

### 任务调度优化
- **并发控制**: 限制同时执行的任务数量
- **优先级队列**: 重要任务优先处理
- **资源监控**: 动态调整任务执行频率
- **负载均衡**: 在多个调度器实例间分配任务

### 内存管理
- **垃圾回收**: 定期触发Python垃圾回收
- **对象池**: 重用频繁创建的对象
- **内存监控**: 实时监控内存使用情况
- **内存泄漏检测**: 定期检查内存泄漏

## 🚀 部署最佳实践

### 生产环境配置
```bash
# 使用systemd服务
sudo cp soluna-scheduler.service /etc/systemd/system/
sudo systemctl enable soluna-scheduler
sudo systemctl start soluna-scheduler

# 配置日志轮转
sudo cp logrotate.conf /etc/logrotate.d/soluna-scheduler
```

### 高可用部署
```yaml
# docker-compose.yml
version: '3.8'
services:
  scheduler-primary:
    image: soluna-scheduler:latest
    environment:
      - ROLE=primary
    volumes:
      - ./.env:/app/.env
      - ./logs:/app/logs
  
  scheduler-backup:
    image: soluna-scheduler:latest
    environment:
      - ROLE=backup
    volumes:
      - ./.env:/app/.env
      - ./logs:/app/logs
```

### 监控集成
```python
# 集成Prometheus监控
from prometheus_client import Counter, Histogram, Gauge

# 定义监控指标
event_counter = Counter('events_generated_total', 'Total events generated')
event_duration = Histogram('event_generation_duration_seconds', 'Time spent generating events')
active_characters = Gauge('active_characters', 'Number of active characters')
```

## 🔮 未来规划

### 短期目标 (1-2个月)
- [ ] 支持多实例部署的分布式锁
- [ ] 更细粒度的任务监控和告警
- [ ] 任务执行历史查询界面
- [ ] 支持自定义任务插件
- [ ] 集成Prometheus和Grafana

### 中期目标 (2-4个月)
- [ ] 支持Kubernetes部署
- [ ] 实时任务状态同步
- [ ] 智能任务调度算法
- [ ] 支持多云部署
- [ ] 任务优先级动态调整

### 长期目标 (4-6个月)
- [ ] 机器学习优化调度策略
- [ ] 支持事件预测和预调度
- [ ] 自适应资源管理
- [ ] 支持事件链和复杂工作流
- [ ] 企业级任务编排平台

## 🤝 贡献指南

### 开发环境设置
1. Fork 项目
2. 创建虚拟环境: `python -m venv venv`
3. 激活环境: `source venv/bin/activate`
4. 安装依赖: `pip install -r requirements.txt`
5. 配置环境: `cp .env.example .env`

### 代码规范
- 遵循PEP 8 Python编码规范
- 使用类型注解
- 添加docstring文档
- 编写单元测试
- 保持代码简洁清晰

### 提交规范
- 使用有意义的提交信息
- 每个提交保持原子性
- 添加适当的测试用例
- 更新相关文档

### 测试要求
- 所有新功能必须包含单元测试
- 集成测试覆盖率 > 80%
- 性能测试通过标准
- 内存泄漏检查

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。

## 💬 联系方式

- 项目主页: https://github.com/yourusername/soluna-scheduler
- 问题反馈: https://github.com/yourusername/soluna-scheduler/issues
- 邮件联系: scheduler@soluna.dev
- 技术支持: support@soluna.dev

---

**Soluna Scheduler** - 让角色世界持续运转的时间引擎
#!/bin/sh

# Docker入口脚本
set -e

# 获取环境类型，默认production
ENVIRONMENT=${ENVIRONMENT:-production}
echo "当前环境: $ENVIRONMENT"

# 尝试从.env文件加载，但不强制
if [ -f ".env.${ENVIRONMENT}" ]; then
    echo "尝试从.env.${ENVIRONMENT}加载配置..."
    # 安全地加载环境变量
    while IFS='=' read -r key value; do
        # 跳过注释和空行
        case $key in
            \#* | '') continue ;;
        esac
        # 移除引号并设置变量
        value=$(echo "$value" | sed 's/^["\x27]//;s/["\x27]$//')
        export "$key=$value"
    done < ".env.${ENVIRONMENT}"
else
    echo "未找到.env.${ENVIRONMENT}，使用Docker环境变量"
fi

# 检查必要的环境变量
echo "检查必要的环境变量..."
required_vars="SOLUNA_API_URL SOLUNA_BATCH_GENERATE_ENDPOINT"

missing_vars=""
for var in $required_vars; do
    eval value=\$${var}
    if [ -z "$value" ]; then
        missing_vars="$missing_vars $var"
    else
        echo "✓ $var: $value"
    fi
done

if [ -n "$missing_vars" ]; then
    echo "错误: 缺少必要的环境变量:$missing_vars"
    exit 1
fi

echo "所有必要的环境变量已配置完成"

# 启动调度器
echo "启动Soluna调度器..."
exec python scheduler.py
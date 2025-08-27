#!/bin/bash

# Soluna Scheduler启动脚本

# 设置脚本执行选项：-e（出错立即退出）、-u（使用未初始化变量时报错）、-o pipefail（管道命令中任一命令失败则整体失败）
set -euo pipefail

# 定义颜色变量，用于美化输出
green="\033[0;32m"
red="\033[0;31m"
yellow="\033[0;33m"
reset="\033[0m"

# 默认虚拟环境路径
VENV_DIR="./venv"

# 显示帮助信息
show_help() {
    echo "${green}Soluna Scheduler启动脚本${reset}"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help            显示帮助信息"
    echo "  --venv <路径>         指定虚拟环境路径 (默认: ./venv)"
    echo "  --install-deps        只安装依赖，不启动服务"
    echo "  --skip-venv           跳过虚拟环境检查和激活"
    echo ""
}

# 解析命令行参数
INSTALL_DEPS_ONLY=false
SKIP_VENV=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        --venv)
            VENV_DIR="$2"
            shift 2
            ;;
        --install-deps)
            INSTALL_DEPS_ONLY=true
            shift
            ;;
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        *)
            echo "${red}未知选项: $1${reset}"
            show_help
            exit 1
            ;;
    esac
done

# 检查Python环境
echo "${green}检查Python环境...${reset}"
if ! command -v python3 &> /dev/null; then
    echo "${red}错误: 未找到Python3。请先安装Python3。${reset}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d ' ' -f 2)
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d '.' -f 1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d '.' -f 2)

if [[ "$PYTHON_MAJOR" -lt 3 ]] || { [[ "$PYTHON_MAJOR" -eq 3 ]] && [[ "$PYTHON_MINOR" -lt 8 ]]; }; then
    echo "${yellow}警告: Python版本 $PYTHON_VERSION 可能不兼容。建议使用Python 3.8或更高版本。${reset}"
fi

echo "使用Python版本: $PYTHON_VERSION"

# 激活虚拟环境
if [[ "$SKIP_VENV" = false ]]; then
    echo "${green}检查虚拟环境...${reset}"
    if [[ ! -d "$VENV_DIR" ]]; then
        echo "${yellow}虚拟环境不存在，正在创建...${reset}"
        python3 -m venv "$VENV_DIR"
        if [[ $? -ne 0 ]]; then
            echo "${red}错误: 创建虚拟环境失败。${reset}"
            exit 1
        fi
    fi
    
    echo "激活虚拟环境: $VENV_DIR"
    if [[ -f "$VENV_DIR/bin/activate" ]]; then
        # macOS/Linux
        source "$VENV_DIR/bin/activate"
    elif [[ -f "$VENV_DIR/Scripts/activate" ]]; then
        # Windows (Git Bash)
        source "$VENV_DIR/Scripts/activate"
    else
        echo "${red}错误: 无法找到虚拟环境激活脚本。${reset}"
        exit 1
    fi
fi

# 安装依赖
echo "${green}安装依赖...${reset}"
if [[ -f "requirements.txt" ]]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    if [[ $? -ne 0 ]]; then
        echo "${red}错误: 安装依赖失败。${reset}"
        exit 1
    fi
else
    echo "${yellow}警告: 未找到requirements.txt文件。${reset}"
fi

# 如果只是安装依赖，就退出
if [[ "$INSTALL_DEPS_ONLY" = true ]]; then
    echo ""
    echo "${green}依赖安装完成。${reset}"
    exit 0
fi

# 检查.env配置文件
echo "${green}检查配置文件...${reset}"
if [[ ! -f ".env" ]]; then
    echo "${yellow}警告: 未找到.env配置文件，将使用默认配置。${reset}"
fi

# 启动服务
start_scheduler() {
    echo ""
    echo "${green}准备启动Soluna Scheduler...${reset}"
    echo "Soluna Scheduler将在后台运行，按Ctrl+C可以停止服务。"
    echo "日志将输出到控制台和scheduler.log文件中。"
    echo ""
    echo "${yellow}启动服务中...${reset}"
    
    # 启动主程序
    python main.py
    
    # 如果程序退出，检查退出码
    if [[ $? -ne 0 ]]; then
        echo ""
        echo "${red}错误: Soluna Scheduler启动失败。请查看日志了解详细信息。${reset}"
        exit 1
    fi
}

# 启动服务
start_scheduler
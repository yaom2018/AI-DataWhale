@echo off
:: 激活conda环境并切换目录的批处理脚本
:: 使用方法：双击运行此脚本或在命令行中执行

:: 初始化conda环境（根据你的miniconda安装路径调整）
call D:\00Program\miniconda3\Scripts\activate.bat

:: 显示可用的conda环境（可选）
echo 可用的conda环境:
conda env list
echo.

:: 激活指定的conda环境
echo 正在激活环境: py310
call conda activate py310

:: 切换到目标目录
echo 正在切换到目录: AI-FastAPI
cd /d "D:\306Datawhale\AI-FastAPI"

:: 显示当前环境和目录信息
echo.
echo 当前conda环境: %CONDA_DEFAULT_ENV%
echo 当前目录: %CD%
echo.

:: 保持命令窗口打开，方便查看输出（可选）
pause
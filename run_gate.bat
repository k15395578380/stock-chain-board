@echo off
chcp 65001 >nul
call .venv\Scripts\activate.bat

echo [1/3] 校验链文件...
python scripts\validate_chains.py
if errorlevel 1 (
    echo 数据层门禁失败，停止。
    exit /b 1
)

echo [2/3] 运行 golden 评估...
python scripts\run_golden.py
set GATE_RESULT=%errorlevel%

echo [3/3] 失败明细
python scripts\show_fails.py

if %GATE_RESULT% neq 0 (
    echo 评估层门禁失败，查看 artifacts\eval-report\report.json
    exit /b 1
)

echo 门禁通过
exit /b 0
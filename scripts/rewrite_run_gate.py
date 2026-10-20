from pathlib import Path

content = '''@echo off
chcp 65001 >nul
call .venv\\Scripts\\activate.bat

echo [1/4] 校验链文件...
python scripts\\validate_chains.py
if errorlevel 1 (
    echo 数据层门禁失败，停止。
    exit /b 1
)

echo [2/4] 运行规则门禁...
python scripts\\run_golden.py
set GATE_RESULT=%errorlevel%

echo [3/4] 运行 LLM 门禁...
python scripts\\run_llm_golden.py
set LLM_RESULT=%errorlevel%

echo [4/4] 失败明细
python scripts\\show_fails.py

if %GATE_RESULT% neq 0 (
    echo 规则门禁失败，查看 artifacts\\eval-report\\report.json
    exit /b 1
)

if %LLM_RESULT% neq 0 (
    echo LLM 门禁失败，查看 artifacts\\eval-report\\llm_report.json
    exit /b 1
)

echo 门禁通过
exit /b 0
'''

path = Path("run_gate.bat")
path.write_text(content, encoding="utf-8")
print(f"已重写 run_gate.bat，大小 {path.stat().st_size} 字节")
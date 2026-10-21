from pathlib import Path

path = Path(".github/workflows/eval-gate.yml")
text = path.read_text(encoding="utf-8")

# 在 setup-python 之后、validate chains 之前插入安装依赖
anchor = "      - name: Validate chains"
insert = """      - name: Install dependencies
        run: pip install -r requirements.txt
"""

if "Install dependencies" not in text:
    text = text.replace(anchor, insert + anchor, 1)
    path.write_text(text, encoding="utf-8")
    print("已给 CI 加上安装依赖步骤")
else:
    print("已有安装依赖步骤，跳过")
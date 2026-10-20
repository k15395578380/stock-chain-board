from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

# 1. 替换模块级 CHAIN_FILES
old_files = 'CHAIN_FILES = [Path("chains/semiconductor.json"), Path("chains/newenergy.json"),Path("chains/ai_compute.json")]'
new_files = 'from chains_config import CHAIN_FILES, THEME_KEYWORDS as CHAINS_THEME_KEYWORDS'
if old_files not in text:
    raise SystemExit("没找到 CHAIN_FILES 行，请检查实际内容")
text = text.replace(old_files, new_files, 1)

# 2. 替换类里的 THEME_KEYWORDS
old_theme = '''    THEME_KEYWORDS = {
        "半导体": ["semi.eda_ip", "semi.material", "semi.equipment", "semi.ic_design", "semi.wafer_fab", "semi.osat", "semi.end_app"],
        "光伏": ["pv.silicon", "pv.wafer", "pv.cell", "pv.module", "pv.aux", "pv.inverter", "pv.epc"],
        "风电": ["wind.component", "wind.turbine", "wind.farm"],
        "AI算力": ["ai.chip", "ai.optical", "ai.switch", "ai.server", "ai.idc", "ai.app"],
    }'''
new_theme = '    THEME_KEYWORDS = CHAINS_THEME_KEYWORDS'
if old_theme not in text:
    raise SystemExit("没找到 THEME_KEYWORDS 类属性，请检查实际内容")
text = text.replace(old_theme, new_theme, 1)

path.write_text(text, encoding="utf-8")
print("run_golden.py 已改用统一配置")
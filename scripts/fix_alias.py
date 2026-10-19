from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

if "SEGMENT_ALIASES" in text:
    print("已有别名表，跳过")
    raise SystemExit(0)

anchor = '    def __init__(self):'
if anchor not in text:
    raise SystemExit("没找到 __init__")

alias_block = '''    SEGMENT_ALIASES = {
        "AI芯片": "ai.chip", "芯片": "ai.chip", "加速卡": "ai.chip",
        "光模块": "ai.optical", "光器件": "ai.optical",
        "交换机": "ai.switch", "网络设备": "ai.switch",
        "服务器": "ai.server", "整机": "ai.server",
        "IDC": "ai.idc", "算力租赁": "ai.idc", "数据中心": "ai.idc",
        "AI应用": "ai.app", "云服务": "ai.app", "大模型": "ai.app",
    }

    def _match_segments(self, q):
        matched = [seg for seg in self.segments.values() if seg["name"] in q]
        if matched:
            return matched
        hit_ids = []
        for alias, sid in self.SEGMENT_ALIASES.items():
            if alias in q and sid in self.segments and sid not in hit_ids:
                hit_ids.append(sid)
        return [self.segments[sid] for sid in hit_ids]

'''

text = text.replace(anchor, alias_block + anchor, 1)

old_matched = '        matched = [seg for seg in self.segments.values() if seg["name"] in q]'
new_matched = '        matched = self._match_segments(q)'
if old_matched not in text:
    raise SystemExit("没找到 matched 匹配行")
text = text.replace(old_matched, new_matched, 1)

path.write_text(text, encoding="utf-8")
print("已加入 segment 别名匹配")
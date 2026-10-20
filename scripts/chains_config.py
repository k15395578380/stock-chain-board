from pathlib import Path

CHAIN_FILES = [
    Path("chains/semiconductor.json"),
    Path("chains/newenergy.json"),
    Path("chains/ai_compute.json"),
    Path("chains/energy_storage.json"),
]

CHAIN_FILES_MAP = {
    "semiconductor": Path("chains/semiconductor.json"),
    "newenergy": Path("chains/newenergy.json"),
    "ai_compute": Path("chains/ai_compute.json"),
    "energy_storage": Path("chains/energy_storage.json"),
}

THEME_KEYWORDS = {
    "半导体": ["semi.eda_ip", "semi.material", "semi.equipment", "semi.ic_design",
              "semi.wafer_fab", "semi.osat", "semi.end_app"],
    "光伏": ["pv.silicon", "pv.wafer", "pv.cell", "pv.module", "pv.aux",
            "pv.inverter", "pv.epc"],
    "风电": ["wind.component", "wind.turbine", "wind.farm"],
    "AI算力": ["ai.chip", "ai.optical", "ai.switch", "ai.server", "ai.idc", "ai.app"],
    "储能": ["es.cell", "es.pcs", "es.system", "es.epc", "es.operation", "es.recycle"],
}
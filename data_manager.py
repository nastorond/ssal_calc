import json
import os

DATA_FILE = "calculator_data.json"

def save_data(app_vars):
    """입력된 값들과 투명도 값을 JSON 파일에 저장합니다."""
    data = {key: var.get().replace(",", "") if isinstance(var.get(), str) else var.get() 
            for key, var in app_vars.items()}
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_data(app_vars):
    """JSON 파일에서 값을 불러와 입력 칸과 슬라이더에 채웁니다."""
    if not os.path.exists(DATA_FILE):
        return
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            for key, var in app_vars.items():
                var.set(data.get(key, var.get()))
        except (json.JSONDecodeError, KeyError):
            pass
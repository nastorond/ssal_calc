import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys
import os

# 다른 파일에서 함수들을 가져옵니다.
from logic import calculate_profits
from data_manager import save_data, load_data

def resource_path(relative_path):
    """ 빌드된 .exe 내부의 파일 경로를 찾아주는 함수 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CalculatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("비약 수익 계산기 v1.1")

        # [추가] 실행 중인 창의 아이콘을 설정합니다.
        self.root.iconbitmap(resource_path("icons/icon.ico"))

        self.root.attributes('-topmost', True)

        self._create_variables()
        self._create_widgets()
        
        # 데이터를 불러온 후, 불러온 값에도 쉼표 서식을 적용합니다.
        load_data(self.app_vars)
        self._format_all_entries()
        
        self.update_alpha(self.app_vars["alpha"].get())
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _create_variables(self):
        """UI와 연결될 변수들을 생성합니다."""
        self.app_vars = {
            "oil": tk.StringVar(), "item": tk.StringVar(), "stone": tk.StringVar(),
            "celebration": tk.StringVar(), "recharge": tk.StringVar(), "small_recharge": tk.StringVar(),
            "alpha": tk.DoubleVar(value=1.0)
        }
        # 실시간 추적(trace) 기능은 이제 사용하지 않습니다.
        
    def _create_widgets(self):
        """UI 위젯들을 생성하고 배치합니다."""
        main_frame = ttk.Frame(self.root, padding=(10, 10))
        main_frame.pack(fill=BOTH, expand=YES)
        
        alpha_frame = ttk.Frame(main_frame)
        alpha_frame.pack(fill=X, padx=5, pady=(0, 10))
        ttk.Label(alpha_frame, text="투명도 조절:").pack(side=LEFT)
        ttk.Scale(alpha_frame, from_=0.2, to=1.0, variable=self.app_vars["alpha"], command=self.update_alpha).pack(side=LEFT, fill=X, expand=YES, padx=5)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="제작 수익 계산")

        material_frame = ttk.LabelFrame(tab1, text=" 재료 가격 입력 ", padding=10)
        material_frame.pack(fill=X, padx=10, pady=5)
        # 각 입력 칸을 self 변수로 저장하여 나중에 접근할 수 있도록 합니다.
        self.oil_entry = self._create_entry(material_frame, "쥬니퍼베리 씨앗 오일:", self.app_vars["oil"])
        self.item_entry = self._create_entry(material_frame, "최상급 아이템 결정:", self.app_vars["item"])
        self.stone_entry = self._create_entry(material_frame, "현자의 돌:", self.app_vars["stone"])

        selling_frame = ttk.LabelFrame(tab1, text=" 완제품 경매장 단가 입력 ", padding=10)
        selling_frame.pack(fill=X, padx=10, pady=5)
        self.celebration_entry = self._create_entry(selling_frame, "경축비:", self.app_vars["celebration"])
        self.recharge_entry = self._create_entry(selling_frame, "재획비:", self.app_vars["recharge"])
        self.small_recharge_entry = self._create_entry(selling_frame, "소형 재획비:", self.app_vars["small_recharge"])
        
        ttk.Button(tab1, text="계산하기", command=self.run_calculation, bootstyle=SUCCESS).pack(fill=X, padx=10, pady=10, ipady=5)
        
        result_frame = ttk.LabelFrame(tab1, text=" 📊 계산 결과 ", padding=10)
        result_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        self.result_label = ttk.Label(result_frame, text="...계산 버튼을 눌러주세요...", font=("-size 16 -weight bold"), anchor=CENTER)
        self.result_label.pack(fill=BOTH, expand=YES)

    def _create_entry(self, parent, label_text, string_var):
        """라벨과 입력 칸을 한 줄에 만들고, FocusOut 이벤트를 바인딩합니다."""
        frame = ttk.Frame(parent)
        frame.pack(fill=X, pady=2)
        ttk.Label(frame, text=label_text, width=20).pack(side=LEFT, padx=(0, 5))
        entry = ttk.Entry(frame, textvariable=string_var)
        entry.pack(side=LEFT, fill=X, expand=YES)
        # [수정] 입력 칸에서 포커스가 벗어날 때 format_entry 함수를 호출하도록 바인딩
        entry.bind("<FocusOut>", self.format_entry)
        return entry

    # [수정] 포커스가 벗어난 입력 칸의 숫자 서식을 변경하는 함수
    def format_entry(self, event):
        """이벤트가 발생한 위젯의 숫자 서식을 변경합니다."""
        widget = event.widget
        current_value = widget.get()
        cleaned_value = "".join(filter(str.isdigit, current_value))
        if cleaned_value:
            formatted_value = f"{int(cleaned_value):,}"
            widget.delete(0, END)
            widget.insert(0, formatted_value)

    def _format_all_entries(self):
        """프로그램 시작 시 모든 입력 칸의 숫자 서식을 일괄 변경합니다."""
        for entry_widget in [self.oil_entry, self.item_entry, self.stone_entry, 
                             self.celebration_entry, self.recharge_entry, self.small_recharge_entry]:
            current_value = entry_widget.get()
            cleaned_value = "".join(filter(str.isdigit, current_value))
            if cleaned_value:
                formatted_value = f"{int(cleaned_value):,}"
                entry_widget.delete(0, END)
                entry_widget.insert(0, formatted_value)
        
    def update_alpha(self, value):
        self.root.attributes("-alpha", float(value))
        
    def run_calculation(self):
        """계산 버튼을 누르면 로직을 호출하고 결과를 업데이트합니다."""
        # 계산 전에 모든 입력 칸의 서식을 한 번 더 정리합니다.
        self._format_all_entries()
        inputs = {key: var.get() for key, var in self.app_vars.items()}
        result_text, color = calculate_profits(inputs)
        self.result_label.config(text=result_text, foreground=color)
        
    def on_closing(self):
        save_data(self.app_vars)
        self.root.destroy()
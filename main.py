import ttkbootstrap as ttk
from ui import CalculatorUI

if __name__ == "__main__":
    # 'cyborg' 테마를 사용하는 ttkbootstrap 창 생성
    root = ttk.Window(themename="litera")
    app = CalculatorUI(root)
    root.mainloop()
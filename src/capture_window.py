import tkinter as tk

class CaptureWindow:
    def __init__(self, min_x, min_y, max_x, max_y):
        # Tkinter root 창 생성
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry(f"{max_x - min_x}x{max_y - min_y}+{min_x}+{min_y}")
        self.root.attributes('-alpha', 0.5)
        self.root.attributes('-topmost', True)
        self.root.withdraw()  # 시작 시 root 창을 숨김

        # 캔버스 생성
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def show(self):
        self.root.after(0, lambda: self.root.deiconify())

    def hide(self):
        self.root.withdraw()

    def start_main_loop(self):
        self.root.mainloop()
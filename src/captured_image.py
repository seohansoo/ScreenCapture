from PIL import ImageTk
import tkinter as tk

class CapturedImage:
    def __init__(self, parent, image, x, y):
        self.parent = parent  # 이미지를 표시할 부모 창 (root)
        self.image = image  # PIL 이미지 객체
        self.x = x  # 이미지 표시할 X 좌표
        self.y = y  # 이미지 표시할 Y 좌표
        self.image_window = None  # 이미지 표시할 윈도우
        self.image_tk = None  # Tkinter용 이미지 객체
        self.drag_data = {"x": 0, "y": 0}  # 드래그 데이터

    def display_image(self):
        # 새로운 창 생성
        self.image_window = tk.Toplevel(self.parent)
        self.image_window.overrideredirect(True)
        self.image_window.attributes('-topmost', True)

        # 이미지를 Tkinter에 맞는 형식으로 변환
        self.image_tk = ImageTk.PhotoImage(self.image)
        label = tk.Label(self.image_window, image=self.image_tk)
        label.image = self.image_tk  # 참조 유지
        label.pack()

        # 창 크기를 이미지 크기에 맞추기
        self.image_window.geometry(f"{self.image.width}x{self.image.height}+{self.x+10}+{self.y+10}")

        # 이미지 드래그 기능 추가
        self.image_window.bind("<ButtonPress-1>", self.on_drag_start)
        self.image_window.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        # 드래그 시작 시점의 좌표 저장
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.image_window.lift()  # 클릭한 이미지를 최상위로 이동

    def on_drag_motion(self, event):
        # 드래그 중일 때 윈도우의 좌표를 이동
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.image_window.geometry(f"+{self.image_window.winfo_x() + delta_x}+{self.image_window.winfo_y() + delta_y}")

    def destroy(self):
        self.image_window.destroy()

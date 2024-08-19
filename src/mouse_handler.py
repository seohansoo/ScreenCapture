from pynput.mouse import Listener as MouseListener, Button

class MouseHandler:
    def __init__(self, capture_manager):
        self.capture_manager = capture_manager
        self.listener = MouseListener(on_click=self.on_click, on_move=self.on_move)
        self.is_dragging = False

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def on_click(self, x, y, button, pressed):
        x_canvas = x - self.capture_manager.min_x
        y_canvas = y - self.capture_manager.min_y    

        if button == Button.left and pressed:
            # 클릭 시작 (드래그 시작)
            self.capture_manager.start_x, self.capture_manager.start_y = x_canvas, y_canvas
            self.is_dragging = True
            self.capture_manager.rect = self.capture_manager.capture_window.canvas.create_rectangle(
                self.capture_manager.start_x, self.capture_manager.start_y,
                self.capture_manager.start_x, self.capture_manager.start_y, outline='red', width=2)
        elif button == Button.left and not pressed:
            # 클릭 종료 (드래그 종료)
            if self.capture_manager.rect is not None:
                self.capture_manager.capture_window.canvas.delete(self.capture_manager.rect)
            self.capture_manager.capture_area(self.capture_manager.start_x + self.capture_manager.min_x,
                                               self.capture_manager.start_y + self.capture_manager.min_y, x, y)
            self.is_dragging = False
            self.capture_manager.capture_window.hide()
            return False

    def on_move(self, x, y):
        if self.is_dragging:
            x_canvas = x - self.capture_manager.min_x
            y_canvas = y - self.capture_manager.min_y
            self.capture_manager.capture_window.canvas.coords(
                self.capture_manager.rect, self.capture_manager.start_x, self.capture_manager.start_y, x_canvas, y_canvas)

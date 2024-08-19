from screeninfo import get_monitors
from mouse_handler import MouseHandler
from keyboard_handler import KeyboardHandler
from capture_window import CaptureWindow
from captured_image import CapturedImage
from PIL import Image
import mss
import sys

class CaptureManager:
    def __init__(self):
        # 화면 초기화
        self.initialize_screen_dimensions()

        # CaptureWindow 객체 생성
        self.capture_window = CaptureWindow(self.min_x, self.min_y, self.max_x, self.max_y)

        # 마우스 및 키보드 핸들러 생성
        self.mouse_handler = None
        self.keyboard_handler = KeyboardHandler(self)

        # 전체 화면 스크린샷 저장
        self.screenshot_full = None
        
        # 이미지 객체 리스트
        self.images = []

    def initialize_screen_dimensions(self):
        monitors = get_monitors()
        self.min_x = min([m.x for m in monitors])
        self.min_y = min([m.y for m in monitors])
        self.max_x = max([m.x + m.width for m in monitors])
        self.max_y = max([m.y + m.height for m in monitors])

    def start_capture(self):
        # 캡처 시작 전 창을 숨김
        self.capture_window.hide()

        # 전체 화면 캡처
        self.capture_full_screen()

        # 캡처 후 창을 다시 보이게 함
        self.capture_window.show()

        # 마우스 리스너 시작
        self.mouse_handler = MouseHandler(self)
        self.mouse_handler.start()

    def capture_full_screen(self):
        with mss.mss() as sct:
            bbox = {'top': self.min_y, 'left': self.min_x, 'width': self.max_x - self.min_x, 'height': self.max_y - self.min_y}
            self.screenshot_full = sct.grab(bbox)
            print("Full screen captured")

    def capture_area(self, x1, y1, x2, y2):
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)

        img = Image.frombytes('RGB', self.screenshot_full.size, self.screenshot_full.rgb)
        cropped_img = img.crop((left - self.min_x, top - self.min_y, right - self.min_x, bottom - self.min_y))

        # CapturedImage 객체 생성 및 표시
        captured_image = CapturedImage(self.capture_window.root, cropped_img, left, top)
        self.capture_window.root.after(0, captured_image.display_image())

        self.images.append(captured_image)

    def exit_program(self):
        print("Exiting...")
        self.capture_window.root.quit()  # Stop Tkinter main loop
        self.capture_window.root.destroy()  # Destroy Tkinter window
        self.keyboard_handler.stop()  # Stop keyboard listener
        sys.exit()  # Exit the program

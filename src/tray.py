import pystray
from PIL import Image, ImageDraw

class Tray:
    def __init__(self, capture_manager):
        self.capture_manager = capture_manager
        # 아이콘 설정
        self.icon = pystray.Icon('ScreenCapture', self.create_image(), 'ScreenCapture')
        self.icon.menu = pystray.Menu(
            pystray.MenuItem('Quit', self.on_quit)  # Quit 버튼 설정
        )

    def run(self):
        self.icon.run()

    def create_image(self):
        # 64x64 아이콘 이미지를 생성합니다
        image = Image.new('RGB', (64, 64), (0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (10, 10, 50, 50),
            fill=(255, 255, 255),
            outline=(0, 0, 0)
        )
        return image

    def on_quit(self, item):
        # 프로그램 종료 로직 실행
        self.capture_manager.capture_window.root.after(0, self.capture_manager.exit_program)
        self.icon.stop()

    def setup(self):
        # 아이콘을 시스템 트레이에 표시
        self.icon.visible = True

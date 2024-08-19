from capture_manager import CaptureManager
import threading
from tray import Tray

def main():
    capture_manager = CaptureManager()
    stray = Tray(capture_manager)
    threading.Thread(target=stray.run).start()
    capture_manager.keyboard_handler.start()
    capture_manager.capture_window.start_main_loop()

if __name__ == "__main__":
    main()

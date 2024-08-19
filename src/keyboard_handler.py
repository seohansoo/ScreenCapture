from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode

class KeyboardHandler:
    def __init__(self, capture_manager):
        self.capture_manager = capture_manager
        self.keys_pressed = set()
        self.listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def on_press(self, key):
        self.keys_pressed.add(key)
        try:
            if Key.alt_l in self.keys_pressed and Key.ctrl_l in self.keys_pressed and any(
                k.vk == 83 for k in self.keys_pressed if isinstance(k, KeyCode)
            ):
                self.capture_manager.capture_window.root.after(0, self.capture_manager.start_capture())
            elif key == Key.up:
                self.capture_manager.capture_window.root.after(0, self.capture_manager.exit_program())
            elif key == Key.esc and self.capture_manager.images:
                image_window = self.capture_manager.images.pop()
                image_window.destroy()
                # self.capture_manager.image_references.pop()
        except Exception as e:
            print(f'Error: {e}')

    def on_release(self, key):
        self.keys_pressed.clear()

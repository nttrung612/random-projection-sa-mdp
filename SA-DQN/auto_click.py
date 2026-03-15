import pyautogui
import time

print("Auto clicker is running. Press Ctrl+C to stop.")

try:
    while True:
        x, y = pyautogui.position()
        pyautogui.click(x, y)
        print(f"Clicked at ({x}, {y})")
        time.sleep(10)
except KeyboardInterrupt:
    print("Auto clicker stopped.")

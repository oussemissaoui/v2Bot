import mss
import numpy as np
import cv2
import pytesseract
import pyautogui

# Function to preprocess the image for better text detection
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    scale_percent = 150
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_LINEAR)
    return resized

# Function to capture and save screenshot and text
def capture_and_save_text():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
        processed_img = preprocess_image(img_np)
        cv2.imwrite("img.png", processed_img)
        print("Processed screen saved as img.png")
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        with open("detected_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Extracted text saved in detected_text.txt")

# Function to search for multiple keywords in the saved text
def search_multiple_words(words_list):
    capture_and_save_text()
    try:
        with open("detected_text.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if any word in the list exists in the text
        for word in words_list:
            if word.lower() in content.lower():
                print(f"'{word}' found in the detected text!")
                pyautogui.hotkey('tab')
                time.sleep(0.5)
                pyautogui.hotkey('tab')
                time.sleep(0.5)
                pyautogui.hotkey('enter')
                
                return True
        
        print("None of the keywords were found in the detected text.")
        return False
    except FileNotFoundError:
        print("detected_text.txt file not found. Make sure to run the capture function first.")
        return False

# Example usage
import time
time.sleep(3)
  # Capture screen and save text
words_to_search = ["Ouvrir Telegram Desktop", "Open Telegram Desktop"]
search_multiple_words(words_to_search)

    
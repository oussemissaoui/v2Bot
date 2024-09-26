import pygetwindow as gw
import time
import gv
import psutil
import os
import threading

import mss
import numpy as np
import cv2
import pytesseract
import pyautogui


def is_telegram_popup_open():
    # Get all windows with "TelegramDesktop" as the exact title
    while not gv.stop_event_CheckP.is_set():
        try:
            windows = gw.getWindowsWithTitle('TelegramDesktop')
            isTrue = False

            if windows:
                # Check if any window has the exact title and is visible and not minimized
                for window in windows:
                    if window.title == "TelegramDesktop" and not window.isMinimized:
                        isTrue = True  # Check if the window is not minimized
                        
            gv.isMoonbix_Open = isTrue
            time.sleep(1)
        except gw.PyGetWindowException as e:
            print(f"Error handling window: {e}. Retrying in 0.5 seconds...")
            time.sleep(1)  # Retry after a short wait
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(1)


def is_window_setup(window_title, x, y, width, height):
    # Get all windows with the specified title
    windows = gw.getWindowsWithTitle(window_title)
    
    # Check each window for position and size
    for window in windows:
        if window.left == x and window.top == y and window.width == width and window.height == height:
            return True
    return False
 
def is_app_running(app_name):
    # Iterate through all running processes
    while not gv.stop_event_CheckT.is_set():
        isTrue = False
        for process in psutil.process_iter(attrs=['pid', 'name']):
            # Check if the process name matches the application name
            if process.info['name'] == app_name:
                isTrue = True
        #print("inside thread")
        gv.isTelegram_exe_open = isTrue
        time.sleep(1)
        
def open_TG_Request():
    timeExecution=time.time()
    isTelegram_Open = False
    while not is_app_running("Telegram.exe") and time.time()-timeExecution < 20 :
        if(isTelegram_Open == False):
            #pyautogui.hotkey('win', 'd')
            time.sleep(1)
            if os.path.exists(gv.telegram_path):
                os.startfile(gv.telegram_path)
                time.sleep(2)
                windows = gw.getWindowsWithTitle("Telegram")
                if windows:
                    telegram_window = windows[0]
                    telegram_window.restore()  # Restore the window if it is minimized
                    telegram_window.activate()  # Bring Telegram Desktop to the foreground
                    print("Telegram Desktop is open and brought to the foreground.")
                    isTelegram_Open = True
                else:
                    print("Telegram Desktop is not open.")
            else:
                print("Telegram Desktop executable not found. Please Download Telegram Desktop")
                
# Function to create and start a single thread
def create_args_th(func, args):
    thread = threading.Thread(target=func, args=args)
    thread.start()
    return thread
def create_noneargs_th(func):
    thread = threading.Thread(target=func)
    thread.start()
    return thread

def get_active_window_title():
    try:
        window = gw.getActiveWindow()
        if window is not None:
            return window.title
        else:
            return "No Active Window"
    except gw.PyGetWindowException as e:
        print(f"Exception: {e}")
        return "Invalid Window Handle"


#check if chrome asking for permission to open TG
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
        #print("Processed screen saved as img.png")
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        with open("detected_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        #print("Extracted text saved in detected_text.txt")

# Function to search for multiple keywords in the saved text
def search_multiple_words(words_list):
    capture_and_save_text()
    try:
        with open("detected_text.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if any word in the list exists in the text
        for word in words_list:
            if word.lower() in content.lower():
                #print(f"'{word}' found in the detected text!")
                gv.isChromeaskingForPermission = True
                return True
        
        #print("None of the keywords were found in the detected text.")
        gv.isChromeaskingForPermission = False
        return False
    except FileNotFoundError:
        #print("detected_text.txt file not found. Make sure to run the capture function first.")
        return False


def all_Checks():
    while not gv.close_event_checking.is_set():
        try:
            windows = gw.getWindowsWithTitle('TelegramDesktop')
            isTrue = False
            if windows:
                # Check if any window has the exact title and is visible and not minimized
                for window in windows:
                    if window.title == "TelegramDesktop" and not window.isMinimized:
                        isTrue = True  # Check if the window is not minimized

            gv.isMoonbix_Open = isTrue
            time.sleep(0.1)
        except gw.PyGetWindowException as e:
            print(f"Error handling window: {e}. Retrying in 0.5 seconds...")
            time.sleep(0.1)  # Retry after a short wait
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(0.1)
        #second
        isTrue = False
        for process in psutil.process_iter(attrs=['pid', 'name']):
            # Check if the process name matches the application name
            if process.info['name'] == "Telegram.exe":
                isTrue = True
        #print("inside thread")
        gv.isTelegram_exe_open = isTrue


        #third
        for process in psutil.process_iter(['name']):
            if process.info['name'] and 'chrome' in process.info['name'].lower():
                active_window_title = get_active_window_title()
                if active_window_title and "Telegram: Contact" in active_window_title:
                    gv.isChromeFocusOnTG = True
                    search_multiple_words(gv.words_to_search)
                    break
                else:
                    gv.isChromeFocusOnTG = False
                    break
            else:
                gv.isChromeFocusOnTG = False

import keyboard      
def key_Board_request():
    while not gv.close_event_keyboard.is_set():
        print("checking keys")
        if keyboard.is_pressed('esc'):
            gv.isRunning = 0
            gv.close_event_keyboard.set()
            gv.close_event_checking.set()
        if keyboard.is_pressed('q'):
            gv.close_event_checking.set()
            gv.thread_checking.join()
        if keyboard.is_pressed('r'):
            if gv.close_event_checking.is_set():
                gv.close_event_checking = threading.Event()
                gv.thread_checking = threading.Thread(target=all_Checks)
                gv.thread_checking.start()
                
        time.sleep(1)
        
    
def pass_chrome_permission():    
    pyautogui.hotkey('tab')
    pyautogui.hotkey('tab')
    time.sleep(0.5)
    pyautogui.hotkey('enter')

def actionBasedOnState():
    if gv.isChromeaskingForPermission == True:
        pass_chrome_permission()
    

def closeAllThreads():
    gv.close_event_keyboard.set()
    gv.close_event_checking.set()
    gv.close_event_action.set()
    gv.thread_action.join()
    gv.thread_checking.join()
    gv.thread_keyboard.join()
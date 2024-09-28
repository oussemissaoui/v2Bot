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
import webbrowser
import platform
import pywinctl
from PIL import Image, ImageDraw
#from test import move_cursor_to_phrase

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
        gv.isChromeaskingForPermission = False
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
                gv.positionMBix = get_window_position_by_name("TelegramDesktop")
        #print("inside thread")
        gv.isTelegram_exe_open = isTrue
        if gv.isTelegram_exe_open == False:
            gv.positionMBix  = (-1, -1, -1, -1)
       
          


        


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
        '''if keyboard.is_pressed('q'):
            gv.close_event_checking.set()
            gv.thread_checking.join()
        if keyboard.is_pressed('r'):
            if gv.close_event_checking.is_set():
                gv.close_event_checking = threading.Event()
                gv.thread_checking = threading.Thread(target=all_Checks)
                gv.thread_checking.start()'''
        if keyboard.is_pressed('g'):
            gv.isGameStart = True
        if keyboard.is_pressed('h'):
            gv.isGameStart = False
                
                
        time.sleep(1)
        
    
def pass_chrome_permission():    
    pyautogui.hotkey('tab')
    time.sleep(0.5)
    pyautogui.hotkey('tab')
    time.sleep(0.5)
    pyautogui.hotkey('enter')

def actionBasedOnState():
    while not gv.close_event_action.is_set():
        if gv.isChromeaskingForPermission == True:
            print("pressing keyyysss")
            pass_chrome_permission()
            gv.isChromeaskingForPermission = False
        if(gv.isMoonbix_Open == False and gv.isChromeFocusOnTG == False):
            if time.time()-gv.LastTimeRunChrome > 10:    
                gv.LastTimeRunChrome = time.time()
                open_MoonBix_in_chrome()
                gv.isChromeClosed = False
        elif gv.isMoonbix_Open == True:
            bring_to_foreground_and_capture("TelegramDesktop", gv.positionMBix) 
            if(gv.isChromeClosed == False):
                close_chrome()
                gv.isChromeClosed = True
        if(gv.isMoonbix_Open ==True and (gv.positionMBix[2]!=100 or gv.positionMBix[3]!=712)):
            gv.globalWin = win32gui.FindWindow(None, "TelegramDesktop")
            if gv.globalWin:
                try:
                     win32gui.SetWindowPos(gv.globalWin, None, 0, 0, 100, 712, win32con.SWP_NOZORDER)
                except TypeError as e:
                    print(f"Error setting window position: {e}")
                else:
                  print("Window handle not found. Ensure the window is open and the title/class name is correct.")
                  
                
        #if(gv.game_level == "Default"):
           # move_cursor_to_phrase(r'imgs\foreground_screenshot.png', "Jouer")
        
        
            
            
        time.sleep(1)


def closeAllThreads():
    gv.close_event_keyboard.set()
    gv.close_event_checking.set()
    gv.close_event_action.set()
    gv.thread_action.join()
    gv.thread_checking.join()
    gv.thread_keyboard.join()

def open_MoonBix_in_chrome():
    url = "https://t.me/Binance_Moonbix_bot/start?startapp=ref_6024980978&startApp=ref_6024980978"
    webbrowser.open(url)

def close_chrome():
    # Get the current operating system
    current_os = platform.system()
    
    if current_os == "Windows":
        # Terminate Chrome processes on Windows
        os.system("taskkill /f /im chrome.exe")
    elif current_os == "Darwin":  # macOS
        # Terminate Chrome processes on macOS
        os.system("pkill -f 'Google Chrome'")
    elif current_os == "Linux":
        # Terminate Chrome processes on Linux
        os.system("pkill -f chrome")
    else:
        print("Unsupported operating system")
        
def get_window_position_by_name(window_name):
    # Find the window by name
    window = pywinctl.getWindowsWithTitle(window_name)
    if window:
        # Return the window's position and size if found
        win = window[0]
        return win.left, win.top, win.width, win.height
    else:
        # Return -1 for all parameters if the window is not found
        return -1, -1, -1, -1
import win32gui
import win32con


def bring_to_foreground_and_capture(window_title, positionMBix):
    # Attempt to find the window
    window = gw.getWindowsWithTitle(window_title)
    if window:
        window = window[0]
        
        # Get the position and size from the tuple
        monitor = {
            "left": positionMBix[0],
            "top": positionMBix[1],
            "width": positionMBix[2],
            "height": positionMBix[3]
        }

        # Capture the screenshot without bringing the window to the foreground
        with mss.mss() as sct:
            try:
                screenshot = sct.grab(monitor)
                # Save the screenshot, overwriting the previous file
                mss.tools.to_png(screenshot.rgb, screenshot.size, output="imgs/foreground_screenshot.png")
                print("Screenshot updated.")
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
    else:
        print("Window not found!")

def move_cursor_to_phrase(image_path, phrase="Jouer", display_result=False):
    """
    This function searches for a specified phrase in the given image and moves the cursor to its position.
    
    Args:
    - image_path (str): The path to the image file.
    - phrase (str): The phrase to search for in the image.
    - display_result (bool): If True, displays the resulting image with highlighted words.
    
    Returns:
    - None
    """
    # Load the image
    image = cv2.imread(image_path)

    # Check if image is loaded properly
    if image is None:
        print(f"Error: Could not load image at {image_path}. Check the file path and file integrity.")
        return

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Start the timer for performance measurement
    start_time = time.time()

    # Use pytesseract to get bounding box data of each word
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    # Initialize variables to track the bounding box of the entire phrase
    x_min, y_min, x_max, y_max = None, None, None, None

    # Search for the phrase in the image
    n_boxes = len(data['text'])
    words_in_phrase = phrase.split()  # Split phrase into individual words for matching
    for i in range(n_boxes):
        word = data['text'][i].strip()
        if word in words_in_phrase:
            # Get the bounding box coordinates
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

            # Update the bounding box for the entire phrase
            if x_min is None or x < x_min:
                x_min = x
            if y_min is None or y < y_min:
                y_min = y
            if x_max is None or (x + w) > x_max:
                x_max = x + w
            if y_max is None or (y + h) > y_max:
                y_max = y + h
            
            # Remove the word from the list to prevent duplicate matches
            words_in_phrase.remove(word)

    # If all words are detected, move the cursor to the center of the phrase
    if x_min is not None and y_min is not None and x_max is not None and y_max is not None:
        cursor_x = (x_min + x_max) // 2
        cursor_y = (y_min + y_max) // 2
        pyautogui.moveTo(cursor_x, cursor_y)
        

    # Check the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

def is_yellow_pixel(hsv_image):
    # Define yellow color range in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    # Create a mask for yellow pixels
    mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    # Return True if any yellow pixels are found
    return np.any(mask)

def check_yellow_in_regions(image_path, allowclick=False):
    # Load the image
    starttime = time.time()
    image = cv2.imread(image_path)
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the regions to check (x, y, width, height)
    first_region = (0+gv.positionMBix[0], 0+gv.positionMBix[1], 25+gv.positionMBix[2], 20+gv.positionMBix[3])
    second_region = (67+gv.positionMBix[0], 0+gv.positionMBix[1], 25+gv.positionMBix[2], 20+gv.positionMBix[3])
    in_between_region = (43+gv.positionMBix[0], 0+gv.positionMBix[1], 4+gv.positionMBix[2], 3+gv.positionMBix[3])
    half_middle = (36+gv.positionMBix[0], 12+gv.positionMBix[1], 20+gv.positionMBix[2], 8+gv.positionMBix[3])



    # Extract regions of interest (ROI)
    roi_first = hsv_image[first_region[1]:first_region[1]+first_region[3], first_region[0]:first_region[0]+first_region[2]]
    roi_second = hsv_image[second_region[1]:second_region[1]+second_region[3], second_region[0]:second_region[0]+second_region[2]]
    roi_in_between = hsv_image[in_between_region[1]:in_between_region[1]+in_between_region[3], in_between_region[0]:in_between_region[0]+in_between_region[2]]
    roi_half_middle = hsv_image[half_middle[1]:half_middle[1]+half_middle[3], half_middle[0]:half_middle[0]+half_middle[2]]

    # Check for yellow pixels in each ROI using vectorized operations
    first_empty = not is_yellow_pixel(roi_first)
    second_empty = not is_yellow_pixel(roi_second)
    yellow_in_between = is_yellow_pixel(roi_in_between)
    half_middle_empty = not is_yellow_pixel(roi_half_middle)

    # Determine if yellow pixels are present in between and other regions are empty
    both_empty = first_empty and second_empty
    #  print(f"yellow in between: {yellow_in_between}, half middle empty: {half_middle_empty}")

    if both_empty and yellow_in_between and half_middle_empty:
            #pyautogui.click(1325, 400)
        pyautogui.click(gv.positionMBix[0]+((gv.positionMBix[2]//2)),gv.positionMBix[1]+((gv.positionMBix[3]//2)))
        print("Click action performed.")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print(f"time taken := {time.time()-starttime}")
    
def capture_screenshot(region, output_filename='screenshot.png'):
    
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_filename)  # Save as PNG
        #print(f"Screenshot saved as {output_filename}")

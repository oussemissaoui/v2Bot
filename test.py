import cv2
import numpy as np
import pyautogui
import time
import mss
import keyboard

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
    first_region = (0, 0, 25, 20)
    second_region = (67, 0, 25, 20)
    in_between_region = (43, 0, 4, 3)
    half_middle = (36, 12, 20, 8)

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
        #pyautogui.click(1325, 400)
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


# Example usage

monitor_region = {"top": 190, "left": 33-22, "width": 80, "height": 20}

import win32con
import win32gui

win32gui.SetWindowPos(win32gui.FindWindow(None, "TelegramDesktop"),None,0,0,100,712,win32con.SWP_NOZORDER)

isrun = True
while isrun:
    capture_screenshot(monitor_region, output_filename='hand.png')
    check_yellow_in_regions("hand.png", allowclick=True)
    if(keyboard.is_pressed('esc')):
        isrun = False
        break

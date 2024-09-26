
import os
import threading
import time 

isRunning=1

window_title = "TelegramDesktop"

isTelegram_exe_open = False
isMoonbix_Open = False
isWindow_Setted_up = False
isChromeFocusOnTG = False
isChromeaskingForPermission = False

close_event_checking = threading.Event()
thread_checking = None

close_event_keyboard = threading.Event()
thread_keyboard = None 

close_event_action = threading.Event() 
thread_action =None


user_profile = os.environ['USERPROFILE']  # Get the path to the current user's profile
telegram_path = os.path.join(user_profile, r"AppData\Roaming\Telegram Desktop\Telegram.exe")

words_to_search = ["Ouvrir Telegram Desktop", "Open Telegram Desktop"]

LastTimeRunChrome = time.time()
isChromeClosed = False
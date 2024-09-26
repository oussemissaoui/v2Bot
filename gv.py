
import os

isRunning=1

window_title = "TelegramDesktop"

isTelegram_exe_open = False
isMoonbix_Open = False
isWindow_Setted_up = False
isChromeFocusOnTG = False
isChromeaskingForPermission = False



user_profile = os.environ['USERPROFILE']  # Get the path to the current user's profile
telegram_path = os.path.join(user_profile, r"AppData\Roaming\Telegram Desktop\Telegram.exe")

words_to_search = ["Ouvrir Telegram Desktop", "Open Telegram Desktop"]
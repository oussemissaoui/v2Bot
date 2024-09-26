from threadsfunc import all_Checks,key_Board_request,actionBasedOnState,closeAllThreads
import gv
import threading
import time



gv.thread_checking = threading.Thread(target=all_Checks)
gv.thread_checking.start()

gv.thread_keyboard = threading.Thread(target=key_Board_request)
gv.thread_keyboard.start()

gv.thread_action = threading.Thread(target=actionBasedOnState)
gv.thread_action.start()



while(gv.isRunning == 1):
  print(f"chrome:{gv.isChromeFocusOnTG}? tg:{gv.isTelegram_exe_open}? moonbix:{gv.isMoonbix_Open}? RequestPermission:{gv.isChromeaskingForPermission} ")
  time.sleep(1)


closeAllThreads()
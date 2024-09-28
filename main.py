from threadsfunc import all_Checks,key_Board_request,actionBasedOnState,closeAllThreads,capture_screenshot
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
  #print(f"chrome:{gv.isChromeFocusOnTG}? tg:{gv.isTelegram_exe_open}? moonbix:{gv.isMoonbix_Open}? RequestPermission:{gv.isChromeaskingForPermission} ")
  #print(f"Window Position and Size: {gv.positionMBix}")
  print(f"posMOONBIX : {gv.positionMBix}")
  print(f"game start ? {gv.isGameStart}")
  #monitor_region = {"top": 200+gv.positionMBix[1], "left": gv.positionMBix[0], "width": 92, "height": 20}
  #if(gv.positionMBix[1] != -1):
    #capture_screenshot(monitor_region,"hand.png")
  
  time.sleep(1)


closeAllThreads()
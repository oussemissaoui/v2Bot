from threadsfunc import all_Checks
import gv



while(gv.isRunning == 1):
  all_Checks()
  print(f"chrome:{gv.isChromeFocusOnTG}? tg:{gv.isTelegram_exe_open}? moonbix:{gv.isMoonbix_Open}? RequestPermission:{gv.isChromeaskingForPermission} ")

from web_socket import LinkyClient
from bosminer import Bosminer
from log import setup_logger
import time
import sys
import os

# --- PATH DEFINES ---
LOGGER_PATH = "/var/log/monitor/monitor.log"
BOSMINER_PATH = "/etc/init.d/bosminer"

# --- EXTRACT VARIABLES FROM ENV ---

# --- DEVICE CONFIGURATION ---
tic_module_port = os.getenv('TIC_MODULE_PORT')
tic_module_ip = os.getenv('TIC_MODULE_IP')

# --- CONSTANTS CONFIGURATION ---
papp_threshold = os.getenv('PAPP_THRESHOLD','100')
integrited_time = os.getenv('INTEGRATED_TIME','5')

#--------------------------------------------
# Moving average Configuration
#--------------------------------------------
NB_MESURES = int(integrited_time)*60    # Number of elements
ALPHA = 2 / (NB_MESURES + 1)            # Coeficient (~0.00133)

# --- LOGGER INITIALISATION ---
LOGGER = setup_logger(LOGGER_PATH,"custom_monitor")

# --- ENTRY POINT ---
if __name__ == "__main__":
    
    # ============================================================
    # CHECK INPUTS
    # ============================================================
    if not tic_module_ip:
        LOGGER.error("TIC_MODULE_IP is not defined")
        sys.exit(1)
    
    if not tic_module_port:
        LOGGER.error("TIC_MODULE_PORT is not defined")
        sys.exit(1)
    
    # ============================================================
    # CONSTRUCTORS
    # ============================================================
    client = LinkyClient(tic_module_ip, tic_module_port)
    bosminer = Bosminer(BOSMINER_PATH)
    
    LOGGER.info("monitor is starting with :")
    LOGGER.info(f"--- TIC MODULE CONFIGURATIONS ---")
    LOGGER.info(f"TIC_MODULE_IP   : '{tic_module_ip}'")
    LOGGER.info(f"TIC_MODULE_PORT : '{tic_module_port}'")
    LOGGER.info(f"--- SCRIPT CONFIGURATION ---")
    LOGGER.info(f"INTEGRATED_TIME : '{integrited_time} minutes'")
    LOGGER.info(f"PAPP_THRESHOLD  : '{papp_threshold} VA'")
    
    papp_moy = 0
    
    while True:
        try:
            if client.s is None:
                if not client.connect():
                    LOGGER.error("Connexion with TIC Module failed")
                    time.sleep(5)
                    continue

            alive = client.update()
            if not alive:
                LOGGER.error("Connexion with TIC Module failed")
                client.s = None # Force reconnexion
                continue

            papp = client.get("PAPP")
            iinst = client.get("IINST")
            ptec = client.get("PTEC")
            if papp.isdigit():
                papp_moy = (ALPHA * int(papp)) + ((1 - ALPHA) * papp_moy)
        except Exception as e:
            print(f"Connexion with TIC Module failed : {e}")

        try:
            if papp_moy == 0 and not bosminer.get_state():
                LOGGER.info(f"Restart mining, the solar panels produce enough power")
                bosminer.restart()
            elif papp_moy >= float(papp_threshold) and bosminer.get_state():
                LOGGER.info(f"Stop mining cause the solar panels are not producing enough power (PAPP : '{int(papp)}VA')")
                bosminer.stop()
        except Exception as e:
            print(f"MAINLY PROCESS : {e}")

        time.sleep(1)
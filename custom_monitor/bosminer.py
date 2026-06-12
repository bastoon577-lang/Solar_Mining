import subprocess
import os

class Bosminer:
    def __init__(self, file_path = "/etc/init.d/bosminer"):
        """ Initialisation de la Classe.
        
        Args:
            file_path (str) : Chemin du fichier de configuration
        """
        if not os.path.exists(file_path):
            raise Exception(f"File '{file_path}' not found.")
        self.file = file_path
        
        # Stop mining immediately
        self.state = False            
        self.stop()
        
    def get_state(self):
        """Getter sur l'état de minage
        
        Return :
            True  -> miner is running
            False -> miner isn't running
        """
        return self.state
        
    def start(self):
        """ Active le service bosminer et démarre l'activité de minage.
        """
        try:
            subprocess.run(
                [self.file, "start"],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise Exception("START command failed")
        self.state = True
        return True
    
    def stop(self):
        """ Arrête le service bosminer et stop l'activité de minage.
        """
        try:
            subprocess.run(
                [self.file, "stop"],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise Exception("STOP command failed")
        self.state = False
        return True
        
    def restart(self):
        """ Redémarre le service bosminer, cette stratégie permet
        de redémarrer le sevice en rechargeant la configuration
        d'origine (Le DPS reprends la puissance maximum).
        """
        try:
            subprocess.run(
                [self.file, "restart"],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise Exception("RESTART command failed")
        self.state = True    
        return True
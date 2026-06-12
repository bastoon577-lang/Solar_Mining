import socket
import json

class LinkyClient:
    def __init__(self, host="192.168.1.16", port=81):
        """ Initialisation de la Classe.
        Args:
            host (str) : Adresse IP ou Hostname
            port (int) : Port de service WebSocket
        """
        self.host = host
        self.port = int(port)
        self.s = None
        self.data_store = {}

    def connect(self):
        """Initialise une connexion persistante.
        """
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(0.1)
            self.s.connect((self.host, self.port))
            
            handshake = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {self.host}:{self.port}\r\n"
                f"Upgrade: websocket\r\n"
                f"Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
                f"Sec-WebSocket-Version: 13\r\n\r\n"
            )
            self.s.send(handshake.encode())
            
            response = self.s.recv(1024).decode()
            if "101 Switching Protocols" in response:
                return True
        except Exception as e:
            raise Exception(f"LinkyClient connexion failed : {e}")
        return False

    def update(self):
        """Lit la socket et met à jour le dictionnaire interne.
        """
        if not self.s:
            return False
            
        try:
            data = self.s.recv(1024)
            if not data:
                return False
                
            offset = 0
            while offset < len(data):
                # Vérification de sécurité : on a besoin d'au moins 2 octets pour l'en-tête
                if len(data) - offset < 2:
                    break
                    
                # Le payload_length est au deuxième octet de chaque trame
                payload_length = data[offset + 1] & 127
                start_payload = offset + 2
                end_payload = start_payload + payload_length
                
                # Extraction et parsing
                json_bytes = data[start_payload:end_payload]
                try:
                    parsed = json.loads(json_bytes.decode('utf-8'))
                    self.data_store.update(parsed)
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    
                    raise Exception(f"LinkyClient Parsing failed : {e}")

                # Déplacement de l'offset pour passer à la trame suivante
                # Chaque trame fait 2 octets (header) + payload_length
                offset = end_payload
                
        except socket.timeout:
            # Pas de nouveau message cette fois-ci, c'est normal (non-bloquant)
            pass
        except (json.JSONDecodeError, UnicodeDecodeError, IndexError):
            pass # Trame corrompue ignorée
            
        return True

    def get(self, key, default=None):
        """Permet de récupérer une valeur stockée.
        
        Args :
            key (str) : La clé.
        """
        val = self.data_store.get(key, default)
        return val
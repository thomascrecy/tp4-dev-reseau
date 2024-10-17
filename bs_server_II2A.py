import argparse
import socket
import psutil
import subprocess
import sys
import datetime
import logging
import time

LOG_DIR = "/var/log/bs_server"
LOG_FILE = "bs_server.log"

class CustomFormatter(logging.Formatter):
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    log_format = "%(asctime)s %(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: log_format,
        logging.INFO: log_format,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M")
        return formatter.format(record)

file_handler = logging.FileHandler(f"{LOG_DIR}/{LOG_FILE}", encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M")
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_local_ips():
    ip_list = []
    ip_info = psutil.net_if_addrs()
    
    for interface, addrs in ip_info.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_list.append(addr.address)

    return ip_list

local_ips = get_local_ips()

# Création d'un objet ArgumentParser
parser = argparse.ArgumentParser(
    description="Démarrer un serveur sur une adresse IP et un port spécifique."
)

# On ajoute la gestion de l'option -l ou --listen
parser.add_argument("-l", "--listen", type=str, action="store", required=True, help="Adresse IP que le serv doit écouter")
parser.add_argument("-p", "--port", type=int, action="store", default=13337, help="Port que le serv doit écouter")

# Permet de mettre à jour notre objet ArgumentParser avec les nouvelles options
args = parser.parse_args()

# Validation de l'adresse IP
try:
    socket.inet_aton(args.listen)
    is_valid_ip = True
except OSError:
    is_valid_ip = False

def is_ip_on_machine(ip):
    # Utilisation de "hostname -I" pour obtenir toutes les adresses IP de la machine
    try:
        ips = subprocess.check_output(['hostname', '-I']).decode('utf-8').split()
        return ip in ips
    except subprocess.CalledProcessError:
        return False

# Initialisation de host et port
host = None
port = args.port  # Défini par défaut

if is_valid_ip:
    if is_ip_on_machine(args.listen):
        host = args.listen
    elif args.listen not in local_ips:
        print(f"ERROR -l argument invalide. L'adresse IP spécifiée {args.listen} n'est pas portée par la machine.")
        sys.exit(4)
else:
    print(f"ERROR -l argument invalide. L'adresse {args.listen} n'est pas une adresse IP valide.")
    sys.exit(3)

# Validation du port
if port < 0 or port > 65535:
    print(f"ERROR -p argument invalide. Le port spécifié {port} n'est pas un port valide (de 0 à 65535).")
    sys.exit(1)

if 0 <= port <= 1024:
    print(f"ERROR -p argument invalide. Le port spécifié {port} est un port privilégié. Spécifiez un port au-dessus de 1024.")
    sys.exit(2)

# On crée un objet socket
# SOCK_STREAM c'est pour créer un socket TCP (pas UDP donc)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On demande à notre programme de se bind sur notre port
s.bind((host, port))  
print("Serveur lancé")

# Place le programme en mode écoute derrière le port auquel il s'est bind
s.listen(1)
logging.info(f"Le serveur tourne sur {host}:{port}")
timeSave = time.time()
# On définit l'action à faire quand quelqu'un se connecte : on accepte
conn, addr = s.accept()
# Dès que quelqu'un se connecte, on affiche un message
print(f"Un client vient de se co et son IP c'est {addr}.")
logging.info(f"Un client ({addr}) s'est connecté.")
timeSave = time.time()

# Petite boucle infinie (bah oui c'est un serveur)
# A chaque itération la boucle reçoit des données et les traite
while True:

    try:
        # On reçoit 1024 bytes de données
        data = conn.recv(1024).decode("utf-8")

        # Si on a rien reçu, on continue
        if not data: break

        # On affiche dans le terminal les données reçues du client
        print(f"Données reçues du client : {data}")
        logging.info(f'Le client {addr} a envoyé "{data}".')

        message = ""
        if "meo" in data:
            message = "Meo à toi confrère."
        elif "waf" in data:
            message = "ptdr t ki"
        else:
            message = "Mes respects humble humain."

        conn.sendall(str.encode(message, "utf-8"))
        logging.info(f'Réponse envoyée au client {addr} : "{message}".')

        # On ferme proprement la connexion TCP
        conn.close()

    except TimeoutError:
        logging.warning("Aucun client depuis plus de une minute.")
        break
    except socket.timeout:
        logging.warning("Aucun client depuis plus de une minute.")
        break
    except socket.error as e:
        print(f"Error Occured: {e}")
        break
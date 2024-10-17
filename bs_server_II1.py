import argparse
import socket
import sys
import subprocess

# Création d'un objet ArgumentParser
parser = argparse.ArgumentParser(
    description="Démarrer un serveur sur une adresse IP et un port spécifique."
)

# On ajoute la gestion de l'option -p ou --port
# "store" ça veut dire qu'on attend un argument à -n
# on va stocker l'argument dans une variable
parser.add_argument("-l", "--listen", type=str, action="store", required=True)
parser.add_argument("-p", "--port", type=int, action="store", default=13337)

parser.add_argument(
    "-l", "--listen", 
    type=str, 
    action="store", 
    required=True,
    help="Adresse IP que le serv doit écouter"
)

parser.add_argument(
    "-p", "--port", 
    type=int, 
    action="store", 
    default=13337, 
    help="Port que le serv doit écouter"
)

# Permet de mettre à jour notre objet ArgumentParser avec les nouvelles options
args = parser.parse_args()

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
    
if is_valid_ip:
    if is_ip_on_machine(args.listen):
        host = args.listen
    else:
        print(f"ERROR -l argument invalide. L'adresse {args.listen} n'est pas l'une des adresses IP de cette machine.")
        sys.exit(4)
else:
    print(f"ERROR -l argument invalide. L'adresse {args.listen} n'est pas une adresse IP valide.")
    sys.exit(3)


if args.port < 0 or args.port > 65535:
    print(f"ERROR -p argument invalide. Le port spécifié {args.port} n'est pas un port valide (de 0 à 65535).")
    sys.exit(1)

elif 0 <= args.port <= 1024:
    print(f"ERROR -p argument invalide. Le port spécifié {args.port} est un port privilégié. Spécifiez un port au dessus de 1024.")
    sys.exit(2)

else :
    port = args.port

# On crée un objet socket
# SOCK_STREAM c'est pour créer un socket TCP (pas UDP donc)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On demande à notre programme de se bind sur notre port
s.bind((host, port))  

# Place le programme en mode écoute derrière le port auquel il s'est bind
s.listen(1)
# On définit l'action à faire quand quelqu'un se connecte : on accepte
conn, addr = s.accept()
# Dès que quelqu'un se connecte, on affiche un message
print(f"Un client vient de se co et son IP c'est {addr}.")

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

        if "meo" in data:
            conn.sendall(str.encode("Meo à toi confrère.", "utf-8"))
        elif "waf" in data:
            conn.sendall(b"ptdr t ki")
        else:
            conn.sendall(b"Mes respects humble humain.")

    except socket.error:
        print("Error Occured.")
        break

# On ferme proprement la connexion TCP
conn.close()

import socket
import sys
import re

# On définit la destination de la connexion
host = '10.4.4.11'  # IP du serveur
port = 13337        # Port choisir par le serveur

# Création de l'objet socket de type TCP (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur
    s.connect((host, port))
    # note : la double parenthèse n'est pas une erreur : on envoie un tuple à la fonction connect()

    # Envoi de data bidon
    print('Que veux-tu envoyer au serveur :')
    message = input()

    if type(message) is not str:
        raise TypeError("C'est pas une string ça")
    elif not re.search("^.*(meo|waf).*$", message):
        raise ValueError("Faut dire meo ou waf en fait")
    
    s.sendall(message.encode('utf-8'))

    # On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
    data = s.recv(1024).decode("utf-8")

    # On libère le socket TCP
    s.close()

    # Affichage de la réponse reçue du serveur
    print(f"Le serveur a répondu {repr(data)}")
    print(f'Connecté avec succès au serveur {host} sur le port {port}')
except Exception as e:
    print('Ca a bug ptdrrr')

sys.exit(0)
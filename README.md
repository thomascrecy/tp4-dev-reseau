# P4 DEV : Socquettes

## I. Simple bs program

## 1. First steps

### 🌞 Commandes...

### Client : 
```
[toto@bsclient b2-resequ-dev-tp4]$ python bs_client_I1.py
Le serveur a répondu b'Hi mate !'
```
### Serveur :
```
[toto@bsserver b2-resequ-dev-tp4]$ sudo firewall-cmd --add-port=13337/tcp --permanent.
[sudo] password for toto: 
success
[toto@bsserver b2-resequ-dev-tp4]$ sudo firewall-cmd --reload
success
[toto@bsserver b2-resequ-dev-tp4]$ sudo firewall-cmd --list-all
[sudo] password for toto:
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3 enp0s8
  sources:
  services: cockpit dhcpv6-client ssh
  ports: 22/tcp 13337/tcp
  protocols:
  forward: yes
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules: 
[toto@bsserver b2-resequ-dev-tp4]$ python bs_server_I1.py
Connected by ('10.4.4.12', 39220)
Données reçues du client : b'Meooooo'
[toto@bsserver b2-resequ-dev-tp4]$ ss -lnpt | grep 13337
LISTEN 0      1          10.4.4.11:13337      0.0.0.0:*    users:(("python",pid=12910,fd=3))
```

## 2. User friendly

### Client :
```
[toto@bsclient b2-resequ-dev-tp4]$ python bs_client_I2.py
Que veux-tu envoyer au serveur :
salut c'est meo
Le serveur a répondu 'Meo à toi confrère.'
Connecté avec succès au serveur 10.4.4.11 sur le port 13337
```
### Serveur :
```
[toto@bsserver b2-resequ-dev-tp4]$ python bs_server_I2.py
Un client vient de se co et son IP c'est ('10.4.4.12', 50236).
Données reçues du client : salut c'est meo
```

## 3. You say client I hear control

# TP4 DEV : Socquettes

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

### Client :
```
[toto@bsclient b2-resequ-dev-tp4]$ python bs_client_I3.py
Que veux-tu envoyer au serveur :
salut c'est meo
Le serveur a répondu 'Meo à toi confrère.'
Connecté avec succès au serveur 10.4.4.11 sur le port 13337
```
### Client erreur : 
```
[toto@bsclient b2-resequ-dev-tp4]$ python bs_client_I3.py
Que veux-tu envoyer au serveur :
Salut c'est moi
Faut dire meo ou waf en fait
Ca a bug ptdrrr
```
### Serveur : 
```
[toto@bsserver b2-resequ-dev-tp4]$ python bs_server_I2.py
Un client vient de se co et son IP c'est ('10.4.4.12', 57980).
```

## II. You say dev I say good practices

## 1. Args

### 🌞 bs_server_II1.py
### [bs_server_II1.py](https://github.com/thomascrecy/b2-resequ-dev-tp4/blob/main/bs_server_II1.py)

## 2. Logs

### A. Logs serveur

### 🌞 bs_server_II2A.py

### [bs_server_II2A.py](https://github.com/thomascrecy/b2-resequ-dev-tp4/blob/main/bs_server_II2A.py)

### B. Logs client

### 🌞 bs_client_II2B.py

### [bs_client_II2B.py](https://github.com/thomascrecy/b2-resequ-dev-tp4/blob/main/bs_client_II2B.py)

## III. COMPUTE
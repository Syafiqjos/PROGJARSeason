import socket
import sys

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('\n>> ');

while True:
    try:
        toBeSend = input()
        client_socket.send(toBeSend.encode())
        data = client_socket.recv(1024)
        decoded_data = data.decode()

        sys.stdout.write(decoded_data)
        sys.stdout.write('\n>> ')
    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)
        break
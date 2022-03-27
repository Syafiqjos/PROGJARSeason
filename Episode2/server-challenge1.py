# server3.py

import socket
import sys
import datetime;

server_address = ('localhost', 5000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

file = open('logs.txt', 'a')

try:
    while True:
        client_socket, client_address = server_socket.accept()
        # print(client_socket, client_address)

        address = client_address[0]
        port = client_address[1]

        ct = datetime.datetime.now()

        data = client_socket.recv(1024).decode()

        print('%s - %s - %s - %s\n' % (address, port, ct, str(data)))
        file.write('%s - %s - %s - %s\n' % (address, port, ct, str(data)))

        client_socket.close()

        # break;

except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)
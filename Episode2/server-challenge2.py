# server-challenge2.py

import socket
import sys
import datetime;

server_address = ('localhost', 5000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

try:
    while True:
        file = open('logs.txt', 'a')

        client_socket, client_address = server_socket.accept()
        # print(client_socket, client_address)

        address = client_address[0]
        port = client_address[1]

        ct = datetime.datetime.now()

        data = client_socket.recv(1024).decode()

        to_be_log = '%s - %s - %s - %s\n' % (address, port, ct, str(data));

        file.write(to_be_log)
        file.close()
        
        if (data == 'asklog'):
            print('Sending Asklog.')
            f = open('logs.txt', 'r')
            log = f.read()
            print(log)

            client_socket.send(log.encode());
        else:
            print('Received: ' + to_be_log)
            client_socket.send(to_be_log.encode())

        # break;
    client_socket.close()

except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)
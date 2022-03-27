# client-challenge2.py

import socket

address = input('Server Address: ')
port = input('Server Port: ')

if address and port:
    while True:
        # localhost 5000
        server_address = (address, int(port))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)

        print('Connected!')

        strsend = input('Send something: ')

        if strsend == 'exit':
            break

        client_socket.send(strsend.encode())
        data = client_socket.recv(4096);

        print('Received:');
        print(data.decode())
        print()
        client_socket.close()
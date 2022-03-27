import socket
import sys
import json

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ');

while True:
    try:
        file_path = str(input())

        # read file without close, with statement will close it for us :)
        with open('client_files/' + file_path, 'r') as f:
            jsonData = {
                'path': file_path,
                'data': f.read()
            }

            toBeSend = json.dumps(jsonData).encode()
            client_socket.send(toBeSend)
            data = client_socket.recv(1024)
            decoded_data = data.decode()
        sys.stdout.write(decoded_data)
        sys.stdout.write('>> ')
    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)
        break
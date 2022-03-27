import socket
import select
import sys
import json

server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

while True:
    try:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                data = sock.recv(1024).decode()
                decoded_peername = str(sock.getpeername())
                jsonData = json.loads(data)

                file_path = 'server_files/' + jsonData['path']
                content = str(jsonData['data'])

                operations = content.split("\n")
                operationsEvaluated = ''

                for operation in operations:
                    if (operation and operation != ''):
                        operationsEvaluated += operation + '=' + str(eval(operation))
                        operationsEvaluated += '\n'

                # write to file using with, no need to close file explicitly
                with open(file_path, 'w') as f:
                    f.write(operationsEvaluated)

                if (data):
                    client_socket.send(data.encode())
                else:
                    sock.close()
                    input_socket.remove(sock)
    except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)
        break
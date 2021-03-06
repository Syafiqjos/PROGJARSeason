import socket
import select
import sys

import os

server_address = ('127.0.0.1', 80)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
server_path = 'server/'

try:
    while True:
        read_ready, write_ready, exception = select.select(
            input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                data = sock.recv(4096).decode()
                print(data)

                request_header = data.split('\r\n')

                try:
                    request_file = request_header[0].split()[1]
                except:
                    continue

                dirs = os.listdir(server_path)
                dirs.insert(0, '..')
                response_header = ''

                filename = request_file[1:]

                if request_file == '/' or request_file == '/index.html':
                    try:
                        f = open(server_path + 'index.html', 'r')
                        response_data = f.read()
                        f.close()
                    except:
                        # index not found, so listing
                        response_data = ''
                        for dir in dirs:
                            response_data += '<a href="/' + dir + '">' + dir + '</a><br/>'

                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: ' + \
                        str(content_length) + '\r\n\r\n'
                else:
                    if os.path.isdir(server_path + filename):
                        dirs = os.listdir(server_path + filename)
                        dirs.insert(0, '..')
                        response_data = ''
                        for dir in dirs:
                            response_data += '<a href="./' + filename + "/" + dir + '">' + dir + '</a><br/>'
                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: ' + \
                            str(content_length) + '\r\n\r\n'
                    elif os.path.isfile(server_path + filename):
                        try:
                            f = open(server_path + filename, 'r')
                            response_data = f.read()
                            f.close()
    
                            content_length = len(response_data)
                            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream; Content-Disposition: attachment; filename="' + filename + '"; charset=utf-8\r\nContent-Length: ' + \
                                str(content_length) + '\r\n\r\n'
                            print (response_header)
                        except:
                            pass

                send_data = response_header.encode() + response_data.encode()
                sock.sendall(send_data)

except KeyboardInterrupt:
    print('\nServer is shutting down...')
    server_socket.close()
    sys.exit()
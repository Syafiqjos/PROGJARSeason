import socket
import select
import sys
from threading import Thread
import json
import os

print('Input main dir path: ')
parent_dir = "D:\\Terkadang\\Aku\\Niat\\Belajar\\Kuliah\\Semester6\\PROGJAR\\Episode5"
main_dir = str(input()) + "_files"

main_dir = os.path.join(parent_dir, main_dir)

try:
	os.mkdir(main_dir)
except:
	pass
print(main_dir + ' directory created.')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))

def send_msg(sock):
	while True:
		full_command = str(input())
		cmd = full_command.split()

		data = ''.encode()

		command = cmd[0]
		if command == 'send':
			file_path = cmd[1]

			with open(main_dir + '/' + file_path, 'r') as f:
				jsonData = {
					'full_command': full_command,
					'command': command,
					'file_path': file_path,
					'body': f.read()
				}

				data = json.dumps(jsonData).encode()
				print(file_path + ' already sent.')
		else:
			jsonData = {
				'full_command': full_command,
				'command': command
			}

			data = json.dumps(jsonData).encode()

		sock.send(data)
		print('<You>', command.strip())

def recv_msg(sock):
	while True:
		data = sock.recv(2048)
		# print(data.decode())

		jsonData = json.loads(data.decode())

		full_command = jsonData['full_command']
		command = jsonData['command']

		if command == 'send':
			file_path = jsonData['file_path']
			body = jsonData['body']

			with open(main_dir + '/' + file_path, 'w') as f:
				f.write(body)

			print('file received.')
		else:
			print(full_command)

Thread(target=send_msg, args=(server,)).start()
Thread(target=recv_msg, args=(server,)).start()

while True:
	sockets_list = [server]
	read_socket, write_socket, error_socket = select.select(sockets_list, [], [])
	for socks in read_socket:
		if socks == server:
			recv_msg(socks)
		else:
			send_msg(socks)

server.close()
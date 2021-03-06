import socket
import select
import sys
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []

def clientthread(conn, addr):
	while True:
		try:
			message = conn.recv(2048).decode()
			if message:
				hasil = str(eval(message)).strip()
				message_to_send =  str(message).strip() + ' = ' + str(hasil).strip()
				message_to_send = '<' + str(addr[0]) + '>' + message_to_send.strip()
				print(message_to_send)
				broadcast(message_to_send, conn)
			else:
				remove(conn)
		except:
			continue

def broadcast(message, connection):
	for clients in list_of_clients:
		if True or clients != connection:
			try:
				# print('sending..')
				# print(message)
				# print('finished sending.')
				clients.send(message.encode())
			except:
				clients.close()
				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print(addr[0] + ' connected')
	threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()
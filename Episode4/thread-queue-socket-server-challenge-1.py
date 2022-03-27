import select
import socket
import sys
import threading

def isprime(num):
    num = int(num)
    for n in range(2,int(num**1/2)+1):
        if num%n==0:
            return False
    return True

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

	 # close all threads
        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self, pl):
        client, address = pl;
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            decoded_data = data.decode()
            numbers = decoded_data.split(", ")

            output = ""

            for i in numbers:
                if isprime(i):
                    output += 'T'
                else:
                    output += 'F'
                output += ", "

            output = output[:-2];
            toBeSend = output.encode()

            print ('recv: ' + str(self.address) + str(toBeSend))
            # print ('recv: ' + str(self.address) + str(data))
            if data:
                self.client.send(toBeSend)
            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    s = Server()
    s.run()
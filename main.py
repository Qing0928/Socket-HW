import socketserver
import socket
import threading
import time
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        connection = self.request
        cur_thread = threading.current_thread()
        print(cur_thread)
        while True:
            data = connection.recv(1024).decode()
            if data == "quit":
                print("client quit")
                break
            self.request.sendall(data.encode())
            print(f"recevice from user:{data}")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    #allow_reuse_address = True

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print("Received: {}".format(response))
    finally:
        sock.close()


if __name__ == "__main__":
    binding = ("", 9999)

    server = ThreadedTCPServer(binding, ThreadedTCPRequestHandler)
    #ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    # Exit the server thread when the main thread terminates
    '''server_thread.daemon = True
    server_thread.start()'''
    while True:
        for i in threading.enumerate():
            print(i)
        time.sleep(5)
    #print("Server loop running in thread:", server_thread.name)

    #client(ip, port, "Hello World 1".encode())
    #client(ip, port, "Hello World 2".encode())
    #client(ip, port, "Hello World 3".encode())

    #server.shutdown()
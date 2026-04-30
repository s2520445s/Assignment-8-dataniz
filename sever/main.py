import socket

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server is running...")

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    data = conn.recv(1024)
    print("Received:", data.decode())
    conn.sendall(b"Data received")
    conn.close()

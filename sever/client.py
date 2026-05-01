import socket

HOST = "127.0.0.1"
PORT = 65432

message = input("Enter your query: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.sendall(message.encode())

data = client.recv(4096)
print("Server response:", data.decode())

client.close()

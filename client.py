import socket

HOST = "SERVER IP ADDRESS" # Server IP Address
PORT = 6564             # Server connection Port

connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_socket.connect((HOST, PORT))

TRANSMIT_DATA = "65636"
def main():
    #socket.connect((HOST, PORT))
    connection_socket.send("Hello World".encode('utf-8'))
    print(connection_socket.recv(1024).decode('utf-8'))

#OBJECTIVE: Send variable value from this client application
if __name__ == "__main__":
    main()


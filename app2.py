import socket

HOST = '172.21.247.212' #"SERVER IP ADDRESS" # Server IP Address
PORT = 6564             # Server connection Port

original = '27岁少妇生孩子后变老'
encoded_original = bytes(original, 'utf-8')
inline_encoded_original = original.encode('utf-8')

connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_socket.connect((HOST, PORT))

TRANSMIT_DATA = "exit"

def socket_deploy():
    #socket.connect((HOST, PORT))
    # connection_socket.send("Hello World".encode('utf-8'))
    connection_socket.send(TRANSMIT_DATA.encode('utf-8'))
    print(connection_socket.recv(1024).decode('utf-8'))

def main():
    socket_deploy()

#OBJECTIVE: Send variable value from this client application
if __name__ == "__main__":
    main()


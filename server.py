import socket, sys, asyncio
import threading, time


#host = socket.gethostbyname(socket.gethostname)
HOST = '172.21.247.212' #'LOCAL IP ADDRESS'
PORT = 6564

TEST_VAR = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(5)

DONE_STATE = False
ECHO_VALUE = True

def worker(text):
    counter = 0
    while not DONE_STATE:
        time.sleep(1)
        counter += 1
        print(f"{text}: {counter}")

async def synchro_test1():
    task = asyncio.create_task(synchro_test2())
    print("Content Set 1")
    await asyncio.sleep(1)
    print("Content Set 2")
    await task

async def synchro_test2():
    print("Second Content Set 1")
    await asyncio.sleep(2)
    print("Second Content Set 2")

def sample_echo(test_var):
    #Test_Value = "Hello World"
    print("Received value: {}".format(test_var))

def toggle_active(input_value):
    if input_value.lower() == "exit":
        DONE_STATE = True


def socket_test_server(seed_var):
    check_var = seed_var
    while not DONE_STATE:
        communication_socket, address = server.accept()
        print("Connection Received from {}".format(address))
        message = communication_socket.recv(65536).decode('utf-8')
        print(f"Message from client is: {message}")
        check_var = message
        communication_socket.send(f"Got your message! Thank You!".encode('utf-8'))
        communication_socket.close()
        print(f"Connection with {address} ended.")

def main():
    while not DONE_STATE:
        TEST_VAR = "VARIABLE_TEXT"
        print(f"SERVER INITIALIZED")
        # threading.Thread(target=worker, daemon=True, args=(TEST_VAR,)).start()        
        #threading.Thread(target=worker, daemon=True, args=("TEST_TEXT",)).start()
        asyncio.run(synchro_test1())
        sthread = threading.Thread(target=socket_test_server, args=(TEST_VAR,), daemon=True)
        sthread_monitor = threading.Thread(target=toggle_active, args=(TEST_VAR,), daemon=True)
        sthread_monitor.start()
        sthread.start()
        # input("Press enter to quit\n")
        # DONE_STATE = True

if __name__ == "__main__":
    main()

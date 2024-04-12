#!/usr/bin/python3
import socket, json, sys, os, subprocess
from svTest import mjTest
from pprint import pprint

AVC_GNR_CPM13 = "10.2.128.88"
WSL_CLIENT = "172.21.247.212"
HOST = AVC_GNR_CPM13 # Server IP Address
PORT = 6564          # Server connection Port

connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_socket.connect((HOST, PORT))

TRANSMIT_DATA = "65636"

#*****************************************************************************
test_results = []

def serialize_mjTest(obj):
    if isinstance(obj, mjTest):
        # Convert all non-serializable fields to a serializable form.
        # For example, converting bytes to strings.
        serialized_data = {}
        for key, value in obj.to_dict().items():
            if isinstance(value, bytes):
                serialized_data[key] = value.decode('utf-8')  # Assuming UTF-8 encoding.
            else:
                serialized_data[key] = value
        return serialized_data
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def create_dictionary(test_log_path):
    values = []
    keys = []
    test_dict = {}
    iterator = 0


    with open(test_log_path, 'r') as sourcefile:
        while True:
        #content = sourcefile.read()
            filepath = sourcefile.readline()
            if not filepath:
                break
            values.append(filepath.strip())
            iterator += 1
    for element in range(len(values)):
        keys.append("key"+str(element))

    for element in range(len(values)):
        for key in keys:
            test_dict[key] = values[element]
    return test_dict

def qat_sample_test(test_file):
    os.symlink(test_file,'/lib/firmware/calgary')
    result = subprocess.run("/svdata/qat_driver/build/cpa_sample_code runTests=16", shell=True, check=True, capture_output=True)
    os.unlink('/lib/firmware/calgary')

def meatjet_sample_test(test_file):
    test_line = "/svdata/meatjet_qat20/seaside/meatjet -stateless -obs=65535 -i {}".format(test_file)
    result = subprocess.run(test_line, shell=True, check=True, capture_output=True, encoding='utf-8')
    return result
#*****************************************************************************
def exec_mj_test():
    test_file_list_path = "/svdata/josephri/SVExec/JUNK/test_content_path.txt"
    test_content = create_dictionary(test_file_list_path)
    for i in range(len(test_content)):
        debug_file = test_content["key{}".format(i)]
        test_object = mjTest(meatjet_sample_test(debug_file))
        #serialize_mjTest(test_object)
        # json.dumps(test_object, default=serialize_mjTest)
        serial_data = json.dumps(test_object, default=serialize_mjTest)
        #test_results.append(json.dumps(test_object, default=serialize_mjTest))
        test_results.append(json.dumps(test_object, default=serialize_mjTest))

    return(test_results)

def send_connection(data, socket):
    connection_socket.send("{}".format(data).encode('utf-8'))
    return(connection_socket.recv(32768).decode('utf-8'))



def main():
    check_val = exec_mj_test()
    debug_value = check_val[0]
    #pprint(check_val[0].data['stdout'])
    sent_var = input("Value to send\n")
    #socket.connect((HOST, PORT))
    #connection_socket.send("Hello World".encode('utf-8'))
    #connection_socket.send("{}".format(TRANSMIT_DATA).encode('utf-8'))
    #pprint(check_val)
    server_response = send_connection(debug_value, connection_socket)
    pprint(server_response)

#OBJECTIVE: Send variable value from this client application
if __name__ == "__main__":
    main()
    
    connection_socket.close()
    sys.exit(0)
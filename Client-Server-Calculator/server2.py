from _thread import *
import sys
import socket

# Function to handle client
def for_handling_client(input_connection,client_address):
    while True:
        # obtain the request
        received_data = input_connection.recv(1024)
        # decode the request which was in encoded format
        decoded_message_data = received_data.decode()
        print("Received: {}".format(decoded_message_data))
        print("from ",client_address)
        # find if the request is not for quitting; if not for quitting, calculate the final answer
        if not decoded_message_data or decoded_message_data == quit:
            break
        answer = calculator(decoded_message_data,client_address)
        # Send Response
        input_connection.send(answer.encode())
    # Close Connection
    input_connection.close()
    print("Disconnected with client", client_address)

#to calculate the final output using eval function of python
def calculator(input,client_address):
    try:
        print("received from ",client_address)
        return str(eval(input))
    except Exception as e:
        
        return "Input not valid as error faced: "+str(e)+" ;try giving proper input message"



# Check if the user entered the correct number of arguments
if len(sys.argv) != 3:
    sys.exit("format of command line argument: python client.py <IP> <Port>")
    
# Get the IP address and port from the command line arguments
server_ip_address = sys.argv[1]
server_port_number = int(sys.argv[2])

if(server_port_number<1024):
    sys.exit("port number cant be below 1024")

#setting up of server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip_address, server_port_number))
#making server ready to accept connection
server_socket.listen(0)
print("Server listening on", server_ip_address, "::", server_port_number)
    
# Process Connections
client_connection = None
try:
    while True:
        # accepting the connection
        client_connection, client_address = server_socket.accept()
        print("Connected with client", client_address) 
        client_connection.send("Server 2".encode())
        # start a new thread for every client, similar to threading in operating system
        start_new_thread(for_handling_client, (client_connection,client_address))
# execute statements if the the Ctrl C exception is caught
except KeyboardInterrupt:
    print("closing the server")

# Close the connection if still existent
if client_connection:
    client_connection.close()

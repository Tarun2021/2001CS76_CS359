import socket
import sys
max_no_of_connections=0
# Function for handling client
def for_handling_client(connection,client_address):
    while True:
        # obtain the request
        data = connection.recv(1024)
        # decode the request
        decoded_message = data.decode()
        print("Received: {}".format(decoded_message))

        # check if the decoded message is not for quitting; if not for quitting, send the message for calculations
        if not decoded_message or decoded_message == quit:
            break
        answer = calculator(decoded_message,client_address)

        # Send Response
        connection.send(answer.encode())

    # closing the connection
    connection.close()
    print("client disconnected with the server")

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
    
# obtain the server's IP address and port number from the command line argument
server_ip_addr = sys.argv[1]
server_port_no = int(sys.argv[2])
if(server_port_no<1024):
    sys.exit("port number cant be below 1024")

# prepare the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip_addr, server_port_no))

#making server ready to accept connection
server_socket.listen(5)
print("Server currently listening on", server_ip_addr, "::", server_port_no)
# to process the connections
try:
    while True:
        
        # accepting the connection 
        client_connection, client_addr = server_socket.accept()
              
        
        print("client having address", client_addr,"connected to server")  
        client_connection.send("Connected with Server 1".encode())
        # separately handle with the client using a function
        for_handling_client(client_connection,client_connection.getpeername())
        
              
# execute statements if the the Ctrl C exception is caught
except KeyboardInterrupt:
    print("closing the server")

# for closing the connection if still exists
if client_connection:
    client_connection.close()

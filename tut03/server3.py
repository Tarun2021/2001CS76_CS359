import socket
import sys
import select

list_of_connections = []

# Function to handle client
def for_handling_client(socket,client_address):
    try:
        encoded_data = socket.recv(1024)

        # Decode Request
        decoded_message = encoded_data.decode()
        print("Received: {}".format(decoded_message))
        print("from ",client_address)

        # Process Request
        if not decoded_message or decoded_message == quit:
            print("Client ( ",client_address," ) Disconnected")
            socket.close()
            list_of_connections.remove(socket)
            return

        answer = calculator(decoded_message,client_address)

        # Send Response
        socket.send(answer.encode())

    except Exception as e:
        print("error {}".format(e))
        socket.close()
        list_of_connections.remove(socket)

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

# setting up of socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip_address, server_port_number))
server_socket.listen(5)
print("Server listening on", server_ip_address, "::", server_port_number)
outputs=[]    
# Add socket to connections
list_of_connections.append(server_socket)

# Process Connections
try:
    while True:
        # to process many sockets using 'select' function in python 
        readable_sockets_from_list_of_connections, _, _ = select.select(list_of_connections, outputs, list_of_connections)
        for socket in readable_sockets_from_list_of_connections:
            # If Server Socket, Accept Connection
            if socket == server_socket:
                client_socket, client_address = server_socket.accept()
                list_of_connections.append(client_socket)
                print("Client ( ",client_address, " ) connected")
                client_socket.send("Server 3".encode())
            # if it is a client socket, process the request
            else:
                for_handling_client(socket,socket.getpeername())
# execute statements if the the Ctrl C exception is caught
except KeyboardInterrupt:
    print("closing the server")

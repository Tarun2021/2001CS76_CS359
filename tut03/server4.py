import socket
import sys
import select

list_of_connections = []
# Function to handle client
def for_handling_client(socket,client_address):
    try:
        data = socket.recv(1024)

        # request to be decoded
        decoded_message = data.decode()
        print("Received: {} ".format(decoded_message))
        print("from ",client_address)

        # Process Request
        if not decoded_message or decoded_message == quit:
            print("Client ",client_address," Disconnected")
            socket.close()
            list_of_connections.remove(socket)
            return

        # Send Response
        socket.send(decoded_message.encode())
    except Exception as e:
        print("error {}".format(e))
        socket.close()
        list_of_connections.remove(socket)

# Check if the user entered the correct number of arguments
if len(sys.argv) != 3:
    sys.exit("format of command line argument: python client.py <IP> <Port>")
    
# obtain the port number and IP address from the command line arguments
server_ip_address = sys.argv[1]
server_port_number = int(sys.argv[2])
if(server_port_number<1024):
    sys.exit("port number cant be below 1024")

# Setup Socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip_address, server_port_number))
server_socket.listen(5)
print("Server listening on", server_ip_address, "::", server_port_number)
    
# Add socket to connections
list_of_connections.append(server_socket)
outputs=[]
# Process Connections
try:
    while True:
        # Process Multiple Socket using select
        readable_sockets_from_list_of_connections, _, _ = select.select(list_of_connections,outputs,list_of_connections)
        for socket in readable_sockets_from_list_of_connections:
            
            if socket == server_socket:
                client_socket, client_address = server_socket.accept()
                list_of_connections.append(client_socket)
                print("Client ",client_address, " connected")
                client_socket.send("Server 4".encode())
            # if it is a client socket, process the request
            else:
                for_handling_client(socket,socket.getpeername())
# execute statements if the the Ctrl C exception is caught
except KeyboardInterrupt:
    print("closing the server")

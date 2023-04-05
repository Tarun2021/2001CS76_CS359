import sys
import socket

# Check if the user entered the correct number of arguments
if len(sys.argv) != 3:
    sys.exit("syntax for command line: python client.py <IP> <Port>")
    
# Save the IP address and port number of the server
server_ip_address = sys.argv[1]
server_port_no = int(sys.argv[2])
# Create Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set socket timeout value to 10 seconds
client_socket.settimeout(5)
# Connect to Server
try:
    client_socket.connect((server_ip_address, server_port_no))
    data = client_socket.recv(1024)
    print("{}".format(data.decode()))
except Exception as e:
    sys.exit("unable to connect! try again. \nError: {}".format(e))
    
# Send Data
try:
    while True:
        input_message = input("Enter Message : ")
        
        # Send Request
        client_socket.send(input_message.encode())
        # receive the encoded data from the socket
        encoded_data = client_socket.recv(1024)
        print("Received: {}".format(encoded_data.decode()))
# handling the Ctrl C to exit the program
except KeyboardInterrupt:
    print("\n Bye; nice talking to the server")

# for closing the connection of client
client_socket.close()

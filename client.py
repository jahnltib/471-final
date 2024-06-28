import socket
import sys
import os

# For use in put command
def send_file(socket, file_name):
    # Open the file in binary mode
    with open(file_name, "rb") as file_obj:
        # Read file data
        while chunk := file_obj.read(1234):
            socket.sendall(chunk)

# For use in get command
def receive_file(socket, file_name):
    with open(file_name, "wb") as file_obj:
        while True:
            chunk = socket.recv(1234)
            if not chunk:
                break
            file_obj.write(chunk)
# For use in get & put commands
def setup_data_connection(control_socket):
    port_response = control_socket.recv(1234).decode()
    port = int(port_response.split()[1])
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((control_socket.getpeername()[0], port))
    return data_socket

# Command line argument check
if len(sys.argv) != 3:
    print("USAGE: python client.py <SERVER IP> <SERVER PORT>")
    sys.exit(1)

# Server IP and port
server_ip = sys.argv[1]
server_port = int(sys.argv[2])

# Create command channel socket
command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.connect((server_ip, server_port))

print("Connected to server.")

# Main loop communicates commands to the server
while True:
    # Capture user input
    user_input = input("ftp> ").strip()
    
    # Send command to server
    command_socket.sendall(user_input.encode())
    
    # Quit
    if user_input.lower() == "quit":
        break
    
    # Get command (download file)
    elif user_input.startswith("get"):
        file_name = user_input.split()[1]
        response = command_socket.recv(1234).decode()
        if response == "SUCCESS":
            data_socket = setup_data_connection(command_socket)
            receive_file(command_socket, file_name)
            command_socket.close()
            print(f"{file_name} downloaded successfully.")
        else:
            print(response)
    # Put command (upload file)
    elif user_input.startswith("put"):
        file_name = user_input.split()[1]
        if not os.path.isfile(file_name):
            print("File not found.")
            continue
        response = command_socket.recv(1234).decode()
        if response == "SUCCESS":
            command_socket = setup_data_connection(command_socket)
            send_file(command_socket, file_name)
            command_socket.close()
            print(f"{file_name} uploaded successfully.")
        else:
            print(response)
    # lists files
    elif user_input == "ls":
        response = command_socket.recv(1234).decode()
        if response.startswith("LIST"):
            files = response[5:]
            print("Files on server:")
            print(files)
        else:
            print(response)

# Close command channel connection
command_socket.close()

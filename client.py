import socket
import sys
import os

def send_file(socket, filename):
    with open(filename, "rb") as file_obj:
        while chunk := file_obj.read(1024):
            socket.sendall(chunk)

def receive_file(socket, filename):
    with open(filename, "wb") as file_obj:
        while True:
            chunk = socket.recv(1024)
            if not chunk:
                break
            file_obj.write(chunk)

def setup_data_connection(control_socket):
    port_response = control_socket.recv(1024).decode()
    port = int(port_response.split()[1])
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((control_socket.getpeername()[0], port))
    return data_socket

# Command prompt
def ftp_prompt():
    print("ftp>", end=" ", flush=True)

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

if command_socket:
    print("Connected to server.")
else:
    print("Connection unsuccessful.")
    sys.exit(1)

# print first ftp> prompt
ftp_prompt()

# Main loop to communicate user input with server
while True:
    user_input = input().strip()
    command_socket.sendall(user_input.encode())
    
    if user_input.lower() == "quit":
        break
    # get command
    elif user_input.startswith("get"):
        file_name = user_input.split()[1]
        response = command_socket.recv(1024).decode()
        if response == "SUCCESS":
            data_socket = setup_data_connection(command_socket)
            receive_file(data_socket, file_name)
            data_socket.close()
            print(f"{file_name} downloaded successfully.")
        else:
            print(response)
    # put command
    elif user_input.startswith("put"):
        file_name = user_input.split()[1]
        if not os.path.isfile(file_name):
            print("File not found.")
            ftp_prompt()
            continue
        response = command_socket.recv(1024).decode()
        if response == "SUCCESS":
            data_socket = setup_data_connection(command_socket)
            send_file(data_socket, file_name)
            data_socket.close()
            print(f"{file_name} uploaded successfully.")
        else:
            print(response)
    # prints out a list of all files
    elif user_input == "ls":
        response = command_socket.recv(1024).decode()
        if response.startswith("LIST"):
            files = response[5:]
            print(f"Files on server: {files}")
        else:
            print(response)
    
    ftp_prompt()

# Close command channel connection
command_socket.close()

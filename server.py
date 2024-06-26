# Implementing the server 
import socket
import os
import threading

def handle_client_control(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        command = client_socket.recv(1024).decode()
        if not command:
            break
        print(f"Received command: {command}")
        if command.startswith('get '):
            filename = command[4:]
            send_file(client_socket, filename)
        elif command.startswith('put '):
            filename = command[4:]
            receive_file(client_socket, filename)
        elif command == 'ls':
            list_files(client_socket)
        elif command == 'quit':
            break
        else:
            client_socket.send(b'FAILURE Unknown command')
    client_socket.close()

def send_file(control_socket, filename):
    if not os.path.isfile(filename):
        control_socket.send(b'FAILURE File not found')
        return
    control_socket.send(b'SUCCESS')
    data_socket = setup_data_connection(control_socket)
    with open(filename, 'rb') as f:
        while chunk := f.read(1024):
            data_socket.send(chunk)
    data_socket.close()

def receive_file(control_socket, filename):
    control_socket.send(b'SUCCESS')
    data_socket = setup_data_connection(control_socket)
    with open(filename, 'wb') as f:
        while chunk := data_socket.recv(1024):
            if not chunk:
                break
            f.write(chunk)
    data_socket.close()

def list_files(control_socket):
    files = os.listdir('.')
    control_socket.send(f"LIST {' '.join(files)}".encode())

def setup_data_connection(control_socket):
    ephemeral_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ephemeral_socket.bind(('', 0))
    ephemeral_socket.listen(1)
    port = ephemeral_socket.getsockname()[1]
    control_socket.send(f"PORT {port}".encode())
    data_socket, _ = ephemeral_socket.accept()
    return data_socket

def main():
    server_port = 1234
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    print(f"Server listening on port {server_port}")
    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client_control, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()
import socket


# Setup socket for TCP protocol using IPv4
def start_server():
    host = '127.0.0.1'
    port = 12345

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the address
    server_socket.bind((host, port))

    # Connect one at a time
    server_socket.listen(1)
    print("Waiting for connection...")

    # Accecpt UE5 connection
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    # Receive data
    while True:
        data = conn.recv(1024).decode()  # Determine how much data is recieved
        if not data:
            break  # Stop if no data is received
        print(f"Received from Unreal Engine: {data}")  # This would be the coordinates or other data

    conn.close()


start_server()

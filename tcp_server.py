# TCP Server - Data Checker
# Accepts a client connection, replies whether each received number is even or odd.

import socket
import sys

SERVER_IP = "192.168.10.254"
SERVER_PORT = 12001
BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 60  # close an idle client connection after this many seconds
MAX_INPUT_LEN = 50


def check_number(data):
    """Validate the received bytes and return the reply string."""
    try:
        text = data.decode().strip()
    except UnicodeDecodeError:
        return "ERROR: data is not valid text"
    if not text:
        return "ERROR: empty message"
    if len(text) > MAX_INPUT_LEN:
        return f"ERROR: input longer than {MAX_INPUT_LEN} characters"
    try:
        number = int(text)
    except ValueError:
        return f"ERROR: '{text}' is not an integer"
    return f"{number} is {'EVEN' if number % 2 == 0 else 'ODD'}"


def handle_client(connection_socket, client_address):
    """Serve one client until it disconnects."""
    connection_socket.settimeout(CLIENT_TIMEOUT)
    try:
        while True:
            # 3. Process input and send response
            data = connection_socket.recv(BUFFER_SIZE)
            # 4. Handle disconnects: empty bytes means the client closed (FIN)
            if not data:
                print(f"Client {client_address[0]}:{client_address[1]} disconnected.")
                break
            print(f"Received {data!r} from {client_address[0]}:{client_address[1]}")
            reply = check_number(data)
            connection_socket.sendall(reply.encode())
            print(f"Sent '{reply}'")
    except socket.timeout:
        print(f"Client {client_address[0]}:{client_address[1]} idle too long, closing.")
    except (ConnectionResetError, BrokenPipeError):
        print(f"Client {client_address[0]}:{client_address[1]} reset the connection.")
    finally:
        # 5. Close the connection to this client (not the listening socket)
        connection_socket.close()


def main():
    server_socket = None
    try:
        # 1. Set up a listening socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(1)
        # Short timeout so Ctrl+C is noticed while waiting in accept()
        server_socket.settimeout(1)
        print(f"TCP server listening on {SERVER_IP}:{SERVER_PORT} (Ctrl+C to stop)")

        while True:
            # 2. Accept client connections
            try:
                connection_socket, client_address = server_socket.accept()
            except socket.timeout:
                continue
            print(f"Connection accepted from {client_address[0]}:{client_address[1]}")
            handle_client(connection_socket, client_address)

    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except OSError as e:
        print(f"Socket error: {e}")
        print(f"Check that this machine has the IP {SERVER_IP} and port {SERVER_PORT} is free.")
    finally:
        if server_socket is not None:
            server_socket.close()
            print("TCP server listening socket closed.")


if __name__ == "__main__":
    main()
    sys.exit(0)

# UDP Server - Data Checker
# Receives a number from a client and replies whether it is even or odd.

# 1. Import modules
import socket
import sys

# 2. Server IP and port (see Fig 1 topology)
SERVER_IP = "192.168.10.254"
SERVER_PORT = 12000
BUFFER_SIZE = 2048   # max bytes read in a single recvfrom() call
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


def main():
    server_socket = None
    try:
        # 3. Create a server-side UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 4. Bind the socket to the address and port
        server_socket.bind((SERVER_IP, SERVER_PORT))
        # Short timeout so Ctrl+C is noticed while waiting
        server_socket.settimeout(1)
        print(f"UDP server listening on {SERVER_IP}:{SERVER_PORT} (Ctrl+C to stop)")

        while True:
            # 5. Wait for and receive an incoming UDP datagram
            try:
                data, client_address = server_socket.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                continue
            except ConnectionResetError:
                # Windows: previous reply triggered ICMP port unreachable
                continue

            print(f"Received {data!r} from {client_address[0]}:{client_address[1]}")

            # 6. Process the input and send a response
            reply = check_number(data)
            server_socket.sendto(reply.encode(), client_address)
            print(f"Sent '{reply}' to {client_address[0]}:{client_address[1]}")

    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except OSError as e:
        print(f"Socket error: {e}")
        print(f"Check that this machine has the IP {SERVER_IP} and port {SERVER_PORT} is free.")
    finally:
        # 7. Close the socket to release the port
        if server_socket is not None:
            server_socket.close()
            print("UDP server socket closed.")


if __name__ == "__main__":
    main()
    sys.exit(0)

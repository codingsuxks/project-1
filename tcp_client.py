# TCP Client - Data Checker
# Connects to the server, sends numbers, and displays whether each is even or odd.

# 1. Import modules
import socket
import sys

# 2. Server IP and port (see Fig 1 topology)
SERVER_IP = "192.168.10.254"
SERVER_PORT = 12001
BUFFER_SIZE = 1024
TIMEOUT = 5          # seconds for connect() and recv()
MAX_INPUT_LEN = 50


def get_number():
    """Prompt until the user enters a valid integer or 'quit'."""
    while True:
        text = input("Enter an integer (or 'quit' to exit): ").strip()
        if text.lower() == "quit":
            return None
        if not text:
            print("Input cannot be empty.")
            continue
        if len(text) > MAX_INPUT_LEN:
            print(f"Input too long (max {MAX_INPUT_LEN} characters).")
            continue
        try:
            int(text)
        except ValueError:
            print("Invalid input. Please enter a whole number, e.g. 7 or -12.")
            continue
        return text


def main():
    client_socket = None
    try:
        # Create the TCP socket and connect (three-way handshake happens here)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to TCP server {SERVER_IP}:{SERVER_PORT}")

        while True:
            # 3. Get user input and send it to the server
            number = get_number()
            if number is None:
                break
            client_socket.sendall(number.encode())

            # 4. Receive the reply and display it
            reply = client_socket.recv(BUFFER_SIZE)
            if not reply:
                print("Server closed the connection.")
                break
            print(f"From server: {reply.decode()}")

    except KeyboardInterrupt:
        print("\nClient interrupted by user.")
    except ConnectionRefusedError:
        print("Connection refused. Is the TCP server running?")
    except socket.timeout:
        print(f"Timed out after {TIMEOUT} seconds (server unreachable or not replying).")
    except (ConnectionResetError, BrokenPipeError):
        print("Connection was lost.")
    except socket.gaierror as e:
        print(f"Invalid server address: {e}")
    except OSError as e:
        print(f"Socket error: {e}")
    finally:
        # 5. Close the socket, which also closes the TCP connection (FIN)
        if client_socket is not None:
            client_socket.close()
            print("TCP client socket closed.")


if __name__ == "__main__":
    main()
    sys.exit(0)

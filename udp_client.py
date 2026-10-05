# UDP Client - Data Checker
# Sends a number to the server and displays whether it is even or odd.

# 1. Import modules
import socket
import sys

# 2. Server IP and port (see Fig 1 topology)
SERVER_IP = "192.168.10.254"
SERVER_PORT = 12000
BUFFER_SIZE = 2048
TIMEOUT = 5          # seconds to wait for a reply
MAX_INPUT_LEN = 50   # limit on characters the user can send


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
        # 3. Create a client-side UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 6. Timeout so the client never blocks forever waiting for a reply
        client_socket.settimeout(TIMEOUT)
        print(f"UDP client ready. Server is {SERVER_IP}:{SERVER_PORT}")

        while True:
            # 4. Get user input and send it to the server
            number = get_number()
            if number is None:
                break
            client_socket.sendto(number.encode(), (SERVER_IP, SERVER_PORT))

            # 5. Receive the reply and display it
            try:
                reply, server_address = client_socket.recvfrom(BUFFER_SIZE)
                print(f"From server {server_address[0]}:{server_address[1]} -> {reply.decode()}")
            except socket.timeout:
                print(f"No reply within {TIMEOUT} seconds. The datagram or reply may have been lost.")
            except ConnectionResetError:
                # Windows reports an ICMP 'port unreachable' this way
                print("Server unreachable (is the server running?).")

    except KeyboardInterrupt:
        print("\nClient interrupted by user.")
    except socket.gaierror as e:
        print(f"Invalid server address: {e}")
    except OSError as e:
        print(f"Socket error: {e}")
    finally:
        # 7. Close the socket to release resources
        if client_socket is not None:
            client_socket.close()
            print("UDP client socket closed.")


if __name__ == "__main__":
    main()
    sys.exit(0)

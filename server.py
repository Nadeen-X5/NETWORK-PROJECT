import socket       # Socket library for creating TCP/IP network connections
import threading    # Threading library to handle multiple clients concurrently


def handle_client(conn, addr):
    """Handles all communication with a single connected client.
    This function is executed inside its own thread, allowing
    the server to support multiple clients concurrently. """

    print(f"[NEW CONNECTION] Client {addr} connected.")
    
    connected = True
    while connected:
        try:
            # Receive data from the client
            data = conn.recv(1024)

            # If empty data is received, the client has disconnected
            if not data:
                print(f"[DISCONNECT] Client {addr} disconnected.")
                connected = False
                break

            # Decode and log request
            message = data.decode('utf-8')
            print(f"[{addr}] Request: {message}")

            try:
                # Split received text into base and exponent
                base_str, exp_str = message.split(',')
                base = float(base_str)
                exponent = float(exp_str)

                # Compute the mathematical result
                result = base ** exponent
                response = str(result)

                print(f"[{addr}] Result: {response}")

            except ValueError:
                # Returned when client sends an invalid format
                response = "Error: invalid input! please use 'base,exponent' format."

            # Send the result or error message back to the client
            conn.sendall(response.encode('utf-8'))

        except ConnectionResetError:
            # Triggered when client force closes the connection
            print(f"[ERROR] Connection reset by {addr}.")
            connected = False
            break

    # Close the connection for this specific client
    conn.close()


def start_server():
    """
    Initializes the server socket, listens for incoming connections,
    and assigns each client to a separate thread. This allows the server
    to handle multiple clients simultaneously (Multi threading).
    """
    HOST = '0.0.0.0'
    PORT = 55555

    # Create a TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind to interface and port
        server.bind((HOST, PORT))
        server.listen()
        print(f"[STARTING] Server is listening on port {PORT}")
    except Exception as e:
        print(f"Server bind error: {e}")
        return

    # Main loop to continuously accept clients
    while True:
        # Accept a new client connection
        conn, addr = server.accept()


        # Multy threding implementation:
        # Every client is handled in a dedicated thread, this ensures
        # that the server continues accepting new clients without waiting
        # for others to finish processing.
        # Without threading:
        # The server would block on a single client.
        # With threading:
        # Each client runs independently, enabling simultaneous connections.

        client_thread = threading.Thread(target=handle_client, args=(conn, addr))

        # Start the thread to handle this client
        client_thread.start()

        # Show how many clients are currently active
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()

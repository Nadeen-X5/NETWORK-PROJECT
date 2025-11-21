import socket       # Import socket library to create network connections
import threading    # Import threading to handle multiple clients at the same time

def handle_client(conn, addr):
    """
    This function runs locally inside a separate thread.
    It handles all communication for ONE specific client.
    """
    print(f"[NEW CONNECTION] Client {addr} connected.")
    
    connected = True
    # Keep the connection open for multiple requests 
    while connected:
        try:
            # 1. Receive Data
            # We listen for a message up to 1024 bytes in size
            # This blocks (waits) until the client sends something
            data = conn.recv(1024)
            
            # Check if the client disconnected (sent empty data)
            if not data:
                print(f"[DISCONNECT] Client {addr} disconnected.")
                connected = False
                break

            # 2. Process Data
            # Decode the bytes into a string (e.g., "2,3")
            message = data.decode('utf-8')
            print(f"[{addr}] Received request: {message}")

            try:
                # Split the string by the comma to get the two numbers
                # Expecting format: "base,exponent"
                base_str, exp_str = message.split(',')

                # Convert the string text into actual numbers (floats)
                base = float(base_str)
                exponent = float(exp_str)

                # 3. Perform the Math Calculation
                # Compute the result: result = base^exponent
                result = base ** exponent

                # Prepare response message
                # Convert the numerical result back to a string to send it
                response = str(result)
                
                # show the answer it calculated (e.g., "Sending result: 8.0")
                print(f"[{addr}] Calculated and sending result: {response}")
                
            except ValueError:
                # Handle error if client sends bad data (like "hello" instead of numbers)
                response = "Error: Invalid input format. Please use 'base,exponent'"
                print(f"[{addr}] Input Error. Sending error message.")

            # 4. Send Response
            # Encode the string back to bytes and send it to the client
            conn.sendall(response.encode('utf-8'))

        except ConnectionResetError:
            # This happens if the client forces the window closed
            print(f"[ERROR] Connection was reset by {addr}.")
            connected = False
            break

    # Close the connection for this specific client cleanly
    conn.close()    

def start_server():
    """
    Main function to set up the server and listen for connections.
    """
    # Configuration
    # '0.0.0.0' allows the server to listen to other computers on the LAN
    HOST = '0.0.0.0' 
    # The port number our server will listen on (must match the Client!)
    PORT = 65432     

    # Create the socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    # AF_INET refers to IPv4, SOCK_STREAM refers to TCP protocol [cite: 8]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind the socket to the IP and Port
        server.bind((HOST, PORT))
        
        # Start listening for incoming connections
        server.listen()
        print(f"[STARTING] Server is listening on {HOST}:{PORT}")
    except Exception as e:
        print(f"Error binding server: {e}")
        return

    # Infinite loop to accept new clients continuously
    while True:
        # Accept a new connection
        # 'conn' is the socket object for the user, 'addr' is their IP
        conn, addr = server.accept()
        
        # MULTI-THREADING LOGIC:
        # Instead of processing the client here (which blocks the server),
        # we create a new thread that runs 'handle_client' separately.
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        
        # Start the thread
        thread.start()
        
        # Optional: Print how many threads are running (Subtract 1 for the main server thread)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Standard Python boilerplate to run the start_server function
if __name__ == "__main__":
    start_server()

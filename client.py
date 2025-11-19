import socket
import time

def start_client():
    # Configuration
    # IMPORTANT: Replace this IP with the actual IP address of the computer running server.py
    SERVER_IP = input("Enter the Server IP address (e.g., 192.168.1.5): ")
    SERVER_PORT = 65432

    # Create a TCP/IP socket [cite: 11]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Successfully connected to {SERVER_IP}:{SERVER_PORT}")
        print("Type 'exit' as the base to quit.")

        # Loop to allow multiple requests on the same connection [cite: 20]
        while True:
            # 1. Get user input [cite: 13]
            base = input("\nEnter Base: ")
            if base.lower() == 'exit':
                break
            
            exponent = input("Enter Exponent: ")

            # Prepare the message in format "base,exponent"
            message = f"{base},{exponent}"

            # 2. Send request and Measure RTT [cite: 18]
            start_time = time.time() # Start timer

            # Send data (must be encoded to bytes)
            client_socket.sendall(message.encode('utf-8'))

            # Wait for and receive the response [cite: 17]
            data = client_socket.recv(1024)

            end_time = time.time() # Stop timer

            # 3. Process results
            response = data.decode('utf-8')
            
            # Calculate RTT in seconds
            rtt = end_time - start_time

            # 4. Display output [cite: 19]
            print(f"Computed Result: {response}")
            print(f"Round-Trip Time (RTT): {rtt:.6f} seconds")

    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Make sure it is running and the IP is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection when done
        print("Closing connection...")
        client_socket.close()

if __name__ == "__main__":
    start_client()
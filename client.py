import socket # lets the program create a TCP connection.
import time   # to measure RTT

def start_client():
    # Configuration
    # Ask the user to input the server's IP address
    SERVER_IP = input("Enter the Server IP address (e.g., 192.168.1.5): ")
    SERVER_PORT = 55555

    # Create a TCP/IP socket
    # AF_INET refers to IPv4, SOCK_STREAM refers to TCP protocol 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Successfully connected to HOST {SERVER_IP}: PORT {SERVER_PORT}")
        print("Type 'exit' as the base to quit.")

        # Loop to allow multiple client on the same connection 
        while True:
            # 1. Get input from the user 
            base = input("\nEnter Base: ")
            if base.lower() == 'exit':
                break
            
            exponent = input("Enter Exponent: ")

            # Combine base and exponent into a single message"
            message = f"{base},{exponent}"

            # 2. Send request and Measure RTT 
            start_time = time.time() # Start timer

            # Send the message to the server (encode string to bytes)
            client_socket.sendall(message.encode('utf-8'))

            # Wait to receive the server's response (up to 1024 bytes)
            client_data = client_socket.recv(1024)

            end_time = time.time() # Stop timer

            # 3. Process the received data
            response = client_data.decode('utf-8')
            
            # Calculate RTT (Round-Trip Time) in seconds
            rtt = end_time - start_time

            # 4. Display results to the user 
            print(f"Computed Result: {response}")
            print(f"Round-Trip Time (RTT): {rtt:.6f} seconds")

    # Error handling
    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Make sure it is running and the IP is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket connection when done
        print("Closing connection...")
        client_socket.close()

if __name__ == "__main__":
    start_client()


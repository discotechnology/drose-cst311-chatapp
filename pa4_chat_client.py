#!env python

"""Chat client for CST311 Programming Assignment 4"""
__author__ = "David Rosenfeld"

# Import statements
import socket as s
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = '10.0.200.2'
server_port = 12000

# Thread that will listen for replies and write them to console
def chat_listener(client_socket):
    # Loops endlessly until main thread finishes or the socket has an exception
    while True:
        try:
            # Read response from server
            server_response = client_socket.recv(1024)
            # Decode server response from UTF-8 bytestream
            server_response_decoded = server_response.decode()
            # Print output from server
            print(server_response_decoded)
        except:
            print('The connection has been closed.')
            break
    
# Thread that sends messages to chat server
def chat_sender(client_socket):
    # Display welcome message
    print('Connected to chat!')
    print('Type your message + \"enter\" to send a message, \"bye\" to quit')
    print('---------------------------------------------')
    
    # Loop until we close the connection with 'bye' or there is a socket exception
    while True:
        # Get input from user
        user_input = input('')
    
        try:
            # Set data across socket to server
            # Note: encode() converts the string to UTF-8 for transmission
            client_socket.send(user_input.encode())
            # If last message sent was 'bye', close the connection and finish thread
            if (user_input.lower() == 'bye'):
                print('Exiting the chat.')
                client_socket.close()
                break
        except:
            print('The connection has been closed.')
            break


def main():
    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
  
    try:
    # Establish TCP connection
        client_socket.connect((server_name,server_port))
    except Exception as e:
        log.exception(e)
        log.error("***Advice:***")
        if isinstance(e, s.gaierror):
          log.error("\tCheck that server_name and server_port are set correctly.")
        elif isinstance(e, ConnectionRefusedError):
          log.error("\tCheck that server is running and the address is correct")
        else:
          log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
        exit(8)
    
    # Create a listener thread, mark as daemon to indicate it should stop when the program exits
    listener_thread = threading.Thread(target=chat_listener, args=(client_socket,), daemon=True)
    listener_thread.start()
    
    # Create a thread to send messages
    sender_thread = threading.Thread(target=chat_sender, args=(client_socket,))
    sender_thread.start()
    
    # When sender thread is done, allow process to finish
   
# This helps shield code from running when we import the module
if __name__ == "__main__":
  main()
#!env python

"""Chat server for CST311 Programming Assignment 4"""
__author__ = "David Rosenfeld"

import socket as s
import time
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

# Thread that takes communications from Client X and forwards others
def client_x_handler(client_x_socket, client_y_socket, client_z_socket):
    # Thread loops until connection is closed or socket throws an exception
    while True:
        # Wait for message from Client X
        message = client_x_socket.recv(1024)
        # Decode message and attach username
        new_msg = 'Client X: ' + message.decode()
        # Attempt to send response, thread exits on exception via break condition
        try:
            # If we get the 'bye' message, forward the message to client Y along with a notification that we left, and close the connection
            if message.decode().lower() == 'bye':
                exit_msg = new_msg + '\nClient X has left the chat.'
                log.info("Client X disconnected.")
                try:
                    client_y_socket.send(exit_msg.encode())
                except:
                # Ignore offline members as we leave - needed to make sure we send bye message to both clients
                    pass
                try:
                    client_z_socket.send(exit_msg.encode())
                except:
                    pass
                client_x_socket.close()
                break
            # Otherwise, re-encode and send message
            else:
                client_y_socket.send(new_msg.encode())
                client_z_socket.send(new_msg.encode())
        # Handle exception if any clients have disconnected    
        except:
            log.error('Client X: One or more clients did not recieve message due to disconnections.')
            break
            

# Thread that takes communications from Client Y and forwards to others
# Same logic as above, split off for ease of thread handling
def client_y_handler(client_x_socket, client_y_socket, client_z_socket):
    while True:
        message = client_y_socket.recv(1024)
        new_msg = 'Client Y: ' + message.decode()
        try:
            if message.decode().lower() == 'bye':
                exit_msg = new_msg + '\nClient Y has left the chat.'
                log.info("Client Y disconnected.")
                try:
                    client_x_socket.send(exit_msg.encode())
                except:
                    pass
                try:
                    client_z_socket.send(exit_msg.encode())
                except:
                    pass
                client_y_socket.close()
                break
            else:
                client_x_socket.send(new_msg.encode())
                client_z_socket.send(new_msg.encode())
        except:
            log.error('Client Y: One or more clients did not recieve message due to disconnections.')
            break
            

# Thread that takes communications from Client Y and forwards to others
# Same logic as above, split off for ease of thread handling            
def client_z_handler(client_x_socket, client_y_socket, client_z_socket):
    while True:
        message = client_z_socket.recv(1024)
        new_msg = 'Client Z: ' + message.decode()
        try:
            if message.decode().lower() == 'bye':
                exit_msg = new_msg + '\nClient Z has left the chat.'
                log.info("Client Z disconnected.")
                try:
                    client_x_socket.send(exit_msg.encode())
                except:
                    pass
                try:
                    client_y_socket.send(exit_msg.encode())
                except:
                    pass
                client_z_socket.close()
                break
            else:
                client_x_socket.send(new_msg.encode())
                client_y_socket.send(new_msg.encode())
        except:
            log.error('Client Z: One or more clients did not recieve message due to disconnections.')
            break
            
        
def main():
  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets
  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Assign port number to socket, and bind to chosen port
  server_socket.bind(('',server_port))
  
  # Configure how many requests can be queued on the server at once
  server_socket.listen(2)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))
  
  # Surround with a try-finally to ensure we clean up the socket after we're done
  try:
    # Enter forever loop to listen for requests
    while True:
      # First client to connect is Client X - create socket and print log to console
      client_x_socket, client_x_address = server_socket.accept()
      log.info("Client X connnected at " + str(client_x_address))
      
      # Second connection is Client Y
      client_y_socket, client_y_address = server_socket.accept()
      log.info("Client Y connnected at " + str(client_y_address))
      
      # Third connection is Client Z
      client_z_socket, client_z_address = server_socket.accept()
      log.info("Client Z connnected at " + str(client_z_address))
      
      # Once all sockets are created, offload each into its own separate handler function that runs in a new thread
      thread_x = threading.Thread(target=client_x_handler, args=(client_x_socket, client_y_socket, client_z_socket,))
      thread_x.start()
      
      thread_y = threading.Thread(target=client_y_handler, args=(client_x_socket, client_y_socket, client_z_socket,))
      thread_y.start()
      
      thread_z = threading.Thread(target=client_z_handler, args=(client_x_socket, client_y_socket, client_z_socket,))
      thread_z.start()
      
      
  finally:
    server_socket.close()

if __name__ == "__main__":
  main()

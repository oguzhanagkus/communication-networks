"""
This is my simple ping server which uses UDP instead of ICMP.
It listens given socket. When a packet recieve, server send it back immidiately.
I test it on my local network. So I needed to simulate packet loss.
To do this, it generate a number between 0 and 10.
If this number smaller than 4, the packet will be lost.
In other words, server does not send back the package.

To stop running, press CTRL+C. There is a handler for it. It closes the socket and exit.
"""

import socket, signal, random

# Set global variables
server_address = ("", 12000)
server_socket = None

# If CTRL+C occurs
def signal_handler(signal, frame):
  server_socket.close()
  exit(0)

# Prepare UDP socket
try:
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(server_address)
except Exception as error:
  print("Error occured!", error)
  exit(1)

# Set signal handler
signal.signal(signal.SIGINT, signal_handler)

# Main loop
while True:
  message, address = server_socket.recvfrom(1024)
  print(message.decode())
  
  loss = random.randint(0, 10)
  if loss < 4:
    continue
  
  server_socket.sendto(message, address)

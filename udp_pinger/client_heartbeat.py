"""
  This is a simple heartbeat client It sends signal periodically to server.
"""

import sys, signal, socket, time

# Set global variables
server_address = ("", 13000)
client_socket = None
interval = 5
sequence = 0

# If CTRL+C occurs
def signal_handler(signal, frame):
  print("\nExiting...")
  client_socket.close()
  sys.exit(0)

# Prepare UDP socket
try:
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client_socket.settimeout(1)
except Exception as error:
  print("Error occured!", error)
  sys.exit(1)

# Set signal handler
signal.signal(signal.SIGINT, signal_handler)

while True:
  epoch_time = time.time()
  message = str(sequence) + " - " + str(epoch_time)
  client_socket.sendto(message.encode(), server_address)

  print(message)
  
  sequence += 1
  time.sleep(interval)
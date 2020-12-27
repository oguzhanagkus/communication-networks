"""
  This is a simple heartbeat server. It listens an app which sends signal periodically.
  If there is no signal in specified duration, it is tought as the app is stopped and reported.
"""

import sys, signal, socket
import datetime

# Set global variables
server_address = ("", 13000)
server_socket = None
previous = 0
period = 5
timeout = period * 10
timeout_period = 0

# If CTRL+C occurs
def signal_handler(signal, frame):
  print("\nExiting...")
  server_socket.close()
  sys.exit(0)

# Prepare UDP socket
try:
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(server_address)
  server_socket.settimeout(timeout)
except Exception as error:
  print("Error occured!", error)
  sys.exit(1)

# Set signal handler
signal.signal(signal.SIGINT, signal_handler)

# Main loop
while True:
  try:
    message, address = server_socket.recvfrom(1024)
    temp_time = float(message.decode().split(" - ")[1])
    difference = round(temp_time - previous, 3)

    print(datetime.datetime.now(), "-", end=" ")
    if previous != 0 and difference > period + 0.1:
      missing = difference / period
      print("Heart is beating. But", int(missing), "sequences is lost ({} seconds).".format(difference))
    else:
      print("Heart is beating.")

    previous = temp_time
    timeout_period = 0
  except Exception as error:
    timeout_period += 1
    print(datetime.datetime.now(), "-", end=" ")
    print("Client has been stopped. No heartbeat for {} seconds.".format(timeout * timeout_period))
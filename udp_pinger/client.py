"""
  This is my simple ping client which uses UDP instead of ICMP.
  It sends 10 packets to given address and waits server to send it back.
  It measures the time between sending and recieving back.
  It waits at most 1 second for each packet, it is the timeout value.
  The sequence of 10 packets cannot be interrupted with CTRL+C.
  Finally it prints ping statistics.
"""

import sys, signal, socket, socket, datetime

# Set global variables
server_address = ("", 12000)
client_socket = None
packet_count = 10
rtt_table = []
lost = 0

# If CTRL+C occurs
def signal_handler(signal, frame):
  pass

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

# Sequential package sending
for i in range(1, packet_count + 1):
  temp = datetime.datetime.now()
  message = "sequence={}\ttime={}".format(i, temp)
  client_socket.sendto(message.encode(), server_address)

  try:
    reply_message, temp_address = client_socket.recvfrom(1024)
    duration = datetime.datetime.now() - temp
    rtt_table.append(duration)
    print("sequence={}\ttime={}ms".format(i, duration.microseconds / 1000))
  except socket.timeout:
    print("sequence={}\ttimeout".format(i))
    lost += 1

# Close socket
client_socket.close()

# Calculate statistics
total = datetime.timedelta()
minimum = datetime.timedelta()
maximum = datetime.timedelta()
average = datetime.timedelta()

if len(rtt_table):
  total = sum(rtt_table, datetime.timedelta())
  minimum = min(rtt_table)
  maximum = max(rtt_table)
  average = total / len(rtt_table)

time = lost * 1000 + total.microseconds / 1000

# Print statistics
print("--- ping statistics ---")
print("{} packet/s transmitted, {} recieved, {}% packet loss, time {}ms".format(packet_count, packet_count - lost, lost / packet_count * 100, time))
print("rtt min/avg/max {}/{}/{} ms".format(minimum.microseconds / 1000, average.microseconds / 1000, maximum.microseconds / 1000))
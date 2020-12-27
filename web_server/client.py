"""
  This is my simple web client which uses HTTP headers.
  It sends a request for single web page.
  You can pass arguments from command line.
  Pass 3 arguments or none:
    - first argument: server host
    - second argument: server port
    - third argument: filename / page

  If you do not pass any arguments, it send request to localhost:80/index.html URL.
"""

import sys, socket

# Default arguments
server_host = "localhost"
server_port = 80
filename = "index.html"

# If any argument passed
if len(sys.argv) == 4:
  server_host = sys.argv[1]
  server_port = int(sys.argv[2])
  filename = sys.argv[3]

# Global variables
server_address = (server_host, server_port)
connection = None

# Prepare socket
try:
  connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connection.connect(server_address)
except Exception as error:
  print("Error occured!", error)
  sys.exit(1)

# Prepare headers
request_line = "GET /" + filename + " HTTP/1.1\r\n" 
header_lines = "Host: " + server_host + "\r\n"
header_lines += "Connection: close\r\n"
blank_line = "\r\n"
request_message = request_line + header_lines + blank_line

# Send headers
connection.send(request_message.encode())

# Recieve data
response = ""
while True:
    data = connection.recv(1024).decode()
    if not data:
        break
    response += data 

# Print data
print(response)

# Close socket
connection.close()
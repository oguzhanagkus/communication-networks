"""
  This is my simple web server which uses HTTP headers.
  It accepts only GET method and return the requested html page.
  Since it is a simple multithreaded server, I have only index.html page.
  If you request another page, you will get 404 (Not found).
  If your request include any method rather than GET, you will get 405 (Method not allowed!).
  Unsynchronized simultaneous reads are not a problem, so no need to use syncronization methods.
"""

import sys, signal, socket, threading, datetime

# Set global variables
threads = []
server_socket = None
server_address = ("", 80)

# Signal handler
def signal_handler(signal, frame):
  for thread in threads:
    print(thread.getName())
    thread.join()

  server_socket.close()
  sys.exit(0)

# Thread function
def client_handler(client_socket, address):
  try:
    request = client_socket.recv(1024).decode()
    items = request.split()
      
    request_type = items[0]
    if request_type != "GET":
      raise Exception("Method not allowed!")

    filename = items[1]
    file = open(filename[1:])
    data = file.read()
    file.close()

    # Prepare headers
    status_line = "HTTP/1.1 200 OK\r\n"
    header_lines = "Connection: keep-alive\r\n"
    header_lines += "Date: {}\r\n".format(datetime.datetime.now())
    header_lines += "Server: MyServer\r\n"
    header_lines += "Content-Length: {}\r\n".format(len(data))
    header_lines += "Content-Type: text/html\r\n"
    blank_line = "\r\n"
    response_message = status_line + header_lines + blank_line

    # Send headers
    client_socket.send(response_message.encode())
    
    # Send content of the file
    for i in range(len(data)):
      client_socket.send(data[i].encode())
      
    print(filename + " sent to " + address[0])

  # Print and response error message
  except Exception as error:
    print("Error occured!", error)
    if (error == "Method not allowed!"):
      client_socket.send("HTTP/1.1 405 METHOD NOT ALLOWED\r\n".encode())
    else:
      client_socket.send("HTTP/1.1 404 NOT FOUND\r\n".encode())

  # Close client socket  
  client_socket.shutdown(socket.SHUT_RDWR)
  client_socket.close()

# Main function
def main():
  global threads, server_socket, server_address

  # Prepare socket
  try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(10)
  except Exception as error:
    print("Error occured!", error)
    sys.exit(1)

  # Set signal handler
  signal.signal(signal.SIGINT, signal_handler)

  # Main loop
  while True:
    # Accept a connection
    print("Server is ready!")
    client_socket, address = server_socket.accept()
    client_socket.settimeout(5)

    t = threading.Thread(target=client_handler, args=(client_socket, address,))
    threads.append(t)
    t.start()

if __name__ == "__main__":
  main()
"""
This my simple mail client which uses STMP commands.
It login to a mail server and send mail to given address.

Set your username and password. Then choose mail server. 
Gmail and Office 365 servers are given but you can add another server.
Also update reciever part, subject, and message parts.

TODO:
  - Send images
"""

import socket, ssl, base64
import time, signal

# Set your authentication information
username = "*****"
password = "*****"

# Choose your mail server
gmail = ("smtp.gmail.com", 587)
office = ("smtp.office365.com", 587)
mail_server = gmail

# Set email details
reciever = "agkusoguzhan@gmail.com"
subject = "Test Mail From My Client"
message = "This is my simple SMTP client for term project of CSE476 course.\n\nBest regards.\n\nOguzhan Agkus\n\n"

# Global declaration for using in the functions below
client_socket = None

# After connection established, if server returns unexpected reply then call this function
def exit_handler(message = None, exit_code = 0):
  if message:
    print(message)
  
  client_socket.send("QUIT\r\n".encode())
  client_socket.close()
  exit(exit_code)

# If CTRL+C occurs
def signal_handler(signal, frame):
  exit_handler()

# Establish TCP connection
try:
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(mail_server)
except Exception as error:
  print("Error occured!", error)
  exit(1)

# Set signal handler
signal.signal(signal.SIGINT, signal_handler)

# Get first data
data = client_socket.recv(1024).decode()
print(data)
if data[:3] != "220":
  exit_handler("Reply is not 220 after connection established!", 1)

# Send HELO command
client_socket.send("HELO MYSERVER\r\n".encode())
data = client_socket.recv(1024).decode()
print(data)
if data[:3] != "250":
  exit_handler("Reply is not 250 after hello!", 1)

# Send STARTTLS command, if encryption is possible, start a new session
client_socket.send("STARTTLS\r\n".encode())
data = client_socket.recv(1024).decode()
print(data)
if data[:3] == "220":
  context = ssl._create_stdlib_context(certfile=None, keyfile=None)
  client_socket = context.wrap_socket(client_socket)

  client_socket.send("HELO MYSERVER\r\n".encode())
  data = client_socket.recv(1024).decode()
  print(data)
  if data[:3] != "250":
    exit_handler("Reply is not 250 after TLS connection!", 1)

# Send AUTH command
client_socket.send("AUTH LOGIN\r\n".encode())
data = client_socket.recv(1024).decode()
print(data) # It says send username

# Send username first, encode it using base64
client_socket.send(base64.b64encode(username.encode()))
client_socket.send("\r\n".encode())
data = client_socket.recv(1024).decode()
print(data) # It says send password

# Send password then, encode it using base64
client_socket.send(base64.b64encode(password.encode()))
client_socket.send("\r\n".encode())
data = client_socket.recv(1024).decode()
print(data) # Accepted or failed

if data[:3] != "235":
  exit_handler("Authentication failed!", 1)

# Send MAIL FROM command
client_socket.send("MAIL FROM:<{}>\r\n".format(username).encode())
data = client_socket.recv(1024).decode()
print(data)

# Send RCPT TO command
client_socket.send("RCPT TO:<{}>\r\n".format(reciever).encode())
data = client_socket.recv(1024).decode()
print(data)

# Send DATA command
client_socket.send("DATA\r\n".encode())
data = client_socket.recv(1024).decode()
print(data)

# A timestamp to compare outgoing with incoming mail
timestamp = time.asctime()
print("--> Sent time:", timestamp, end="\n\n")

# Send message data
client_socket.send("Subject: {}\r\n\r\n".format(subject).encode())
client_socket.send(message.encode())
client_socket.send("Sent time: {} \r\n".format(timestamp).encode())
client_socket.send("\r\n.\r\n".encode())
data = client_socket.recv(1024).decode()
print(data)

# Send QUIT command
client_socket.send("QUIT\r\n".encode())
data = client_socket.recv(1024).decode()
print(data)
  
client_socket.close()

print("Successfully completed!")

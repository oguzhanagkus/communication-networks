
"""
  This my simple mail client which uses STMP commands.
  It login to a mail server and send mail to given address.
  Set your username and password. Then choose a mail server. 
  Gmail and Office 365 servers are given but you can add another server.
  Also update the "reciever", "subject", and "message" variables.
  If you want to send an image as an attachment, update "attachment_file" variable wity your image's path.
  If you do not want to send images, set "attachment_file" variable to NoneType object (None).
  It uses MIME protocol to send mail with attachments.
"""

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os, sys, signal, socket, ssl, time, base64

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
attachment_file = "./1.png"

# Global declaration for using in the functions below
client_socket = None
content = None

# After connection established, if server returns unexpected reply then call this function
def exit_handler(message = None, exit_code = 0):
  if message:
    print(message)
  
  client_socket.send("QUIT\r\n".encode())
  client_socket.close()
  sys.exit(exit_code)

# If CTRL+C occurs
def signal_handler(signal, frame):
  exit_handler()

# Establish TCP connection
try:
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(mail_server)
except Exception as error:
  print("Error occured!", error)
  sys.exit(1)

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

# Send username first, encode it with base64
client_socket.send(base64.b64encode(username.encode()))
client_socket.send("\r\n".encode())
data = client_socket.recv(1024).decode()
print(data) # It says send password

# Send password then, encode it with base64
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

# Timestamp to compare outgoing with incoming mail
timestamp = "--> Sent time: " + time.asctime()

# Fill content
content = MIMEMultipart()
content["From"] = "Oguzhan Agkus"
content["To"] = reciever
content["Subject"] = subject

text = MIMEText(message + timestamp)
content.attach(text)

# Attach image
if attachment_file != None:
  try:
    with open(attachment_file, "rb") as image_file:
      image_data = image_file.read()
      image = MIMEImage(image_data, name=os.path.basename(attachment_file))
      content.attach(image)
  except Exception as error:
    print("Cannot add image to mail: ", error)

# Convert MIME object to string
content = content.as_string()

# Send content
client_socket.send(content.encode())
client_socket.send("\r\n.\r\n".encode())
data = client_socket.recv(1024).decode()
print(data)

# Send QUIT command
client_socket.send("QUIT\r\n".encode())
data = client_socket.recv(1024).decode()
print(data)

client_socket.close()

print("Successfully completed!")
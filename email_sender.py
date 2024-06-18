import socket
import ssl
from base64 import b64encode
import pandas as pd

# Email and SMTP server details
userEmail = "useremail@gmail.com"
userPassword = "password"
mailserver = 'smtp.gmail.com'

# Email content
userSubject = input("Enter Subject: ")
userBody = input("Enter Message: ")
msg = '{}.\r\nKeep smiling'.format(userBody)

# Read the Excel file
contacts = pd.read_excel('contacts.xlsx')

# Function to send email
def send_email(sslClientSocket, userDestinationEmail, userSubject, msg):
    mailFromCommand = f"MAIL FROM: <{userEmail}>\r\n"
    sslClientSocket.send(mailFromCommand.encode())
    recv2 = sslClientSocket.recv(1024).decode()
    print(recv2)

    rcptToCommand = f"RCPT TO: <{userDestinationEmail}>\r\n"
    sslClientSocket.send(rcptToCommand.encode())
    recv3 = sslClientSocket.recv(1024).decode()
    print(recv3)

    dataCommand = "DATA\r\n"
    sslClientSocket.send(dataCommand.encode())
    recv4 = sslClientSocket.recv(1024).decode()
    print(recv4)

    sslClientSocket.send(f"Subject: {userSubject}\r\n\r\n{msg}\r\n.\r\n".encode())

# Establish a single connection and send all emails
try:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((mailserver, 587))  # 587 is the default port for SMTP with TLS/STARTTLS

    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    clientSocket.send("STARTTLS\r\n".encode())
    recv2 = clientSocket.recv(1024).decode()
    print(recv2)
    
    # Create SSL context and wrap the socket
    context = ssl.create_default_context()
    sslClientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

    sslClientSocket.send("AUTH LOGIN\r\n".encode())
    print(sslClientSocket.recv(1024))
    sslClientSocket.send(b64encode(userEmail.encode()) + "\r\n".encode())
    print(sslClientSocket.recv(1024))
    sslClientSocket.send(b64encode(userPassword.encode()) + "\r\n".encode())
    print(sslClientSocket.recv(1024))

    # Loop through each contact and send the email
    for index, contact in contacts.iterrows():
        userDestinationEmail = contact['Email']
        print(f"Sending email to {userDestinationEmail}")
        try:
            send_email(sslClientSocket, userDestinationEmail, userSubject, msg)
        except Exception as e:
            print(f"Failed to send email to {userDestinationEmail}. Error: {e}")

    quitCommand = "QUIT\r\n"
    sslClientSocket.send(quitCommand.encode())
    recv5 = sslClientSocket.recv(1024).decode()
    print(recv5)
    sslClientSocket.close()

except Exception as e:
    print(f"An error occurred: {e}")

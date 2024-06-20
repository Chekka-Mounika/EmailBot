import socket
import ssl
from base64 import b64encode
import pandas as pd
import time
import logging
from tenacity import retry, wait_fixed, stop_after_attempt
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, filename='email_bot.log', 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Your email credentials and message details
userEmail = "bugreport.bloodhelp@gmail.com"
userPassword = "noxowkskenumovth"
userSubject = input("Enter Subject: ")
userBody = input("Enter Message: ")

# Read the Excel file
contacts = pd.read_excel('contacts.xlsx')

# SMTP settings
mailserver = 'smtp.gmail.com'
port = 587

# Function to send email
@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def send_email(to_email, subject, body):
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((mailserver, port))
        clientSocket.recv(1024)
        clientSocket.send("HELO Alice\r\n".encode())
        clientSocket.recv(1024)
        clientSocket.send("STARTTLS\r\n".encode())
        clientSocket.recv(1024)
        sslClientSocket = ssl.wrap_socket(clientSocket)
        sslClientSocket.send("AUTH LOGIN\r\n".encode())
        sslClientSocket.recv(1024)
        sslClientSocket.send(b64encode(userEmail.encode()) + b"\r\n")
        sslClientSocket.recv(1024)
        sslClientSocket.send(b64encode(userPassword.encode()) + b"\r\n")
        sslClientSocket.recv(1024)

        mailFromCommand = f"MAIL FROM: <{userEmail}>\r\n"
        sslClientSocket.send(mailFromCommand.encode())
        sslClientSocket.recv(1024)
        rcptToCommand = f"RCPT TO: <{to_email}>\r\n"
        sslClientSocket.send(rcptToCommand.encode())
        sslClientSocket.recv(1024)
        sslClientSocket.send("DATA\r\n".encode())
        sslClientSocket.recv(1024)
        msg = f"Subject: {subject}\r\n\r\n{body}\r\n.\r\n"
        sslClientSocket.send(msg.encode())
        sslClientSocket.recv(1024)
        sslClientSocket.send("QUIT\r\n".encode())
        sslClientSocket.recv(1024)
        sslClientSocket.close()
        logging.info(f"Email successfully sent to {to_email}")
    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {e}")
        raise

# Function to send emails in batches concurrently
def send_emails_in_batch(emails):
    threads = []
    for email in emails:
        thread = threading.Thread(target=send_email, args=(email, userSubject, userBody))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Send emails in batches
batch_size = 10
for i in range(0, len(contacts), batch_size):
    batch = contacts['Email'][i:i+batch_size].tolist()
    logging.info(f"Sending batch {i//batch_size + 1} of {batch_size}")
    send_emails_in_batch(batch)
    time.sleep(5)  # Pause between batches to avoid overwhelming the server


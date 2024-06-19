# BloodHelp Email Reminder Bot

## Table of Contents
1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Features](#features)
5. [Prerequisites](#prerequisites)
6. [Enable SMTP access](#access)
7. [Installation](#installation)
8. [Configuration](#configuration)
9. [Usage](#usage)
10. [Screenshots](#screen)

---

## Introduction
BloodHelp is a platform dedicated to connecting blood donors with recipients efficiently. 

---

## Problem Statement
In closed testing phase , I have to send bulk remainders to all the testers to test the app. As it has been made compulsary for all new developer accounts to go through the phase of closed testing. 

---

## Solution
This Bot uses SMTP protocols from scratch and sends emails to the testers. The efficiency of the bot is increased to 70% by using multi threading and batch techiniques. Used Tenacity to handle transient failures.

---

## Features
- **Automated Email Reminders:** Sends scheduled reminder emails to donors.
- **Integration with Excel:** Reads contact information from an Excel file.
- **SMTP Authentication:** Uses secure authentication to send emails.
- **Error Handling:** Catches and displays errors during the email sending process.

---



### Prerequisites
- Python 3.x
- pandas
- An email server (SMTP)
- An Excel file with contact information
  
---
### access
-Make sure SMTP access is enabled for your email account. For Gmail users, this typically involves allowing "less secure apps" or setting up an App Password if 2-Step Verification is enabled. 

---
### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BloodHelp-email-bot.git
2. Navigate to project directory
   ```bash
   cd BloodHelp-email-bot
3. Install the required packages:
   ```bash
   pip install pandas

---

### Configuration
1. Open the Python script and update the email server settings and user credentials:
  -userEmail = "useremail@gmail.com"
  -userPassword = "password"
  -mailserver = 'smtp.gmail.com'
2. Ensure that your Excel file with contact information is named contacts.xlsx and is placed in the same directory as the script.

---

### Usage
1. Run the script
   ```bash
   python email_bot.py
2. Enter the subject and body of the email when prompted.
3. The bot will read the contact information from contacts.xlsx and send emails accordingly.

---

### screen
1. ScreenShot
![Remainders sent sucessfully](screenshots/run.png)



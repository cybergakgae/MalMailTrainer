#! /usr/bin/python3
#-*- coding:utf-8 -*-

# Copyright (c) 2019 Han Seungyeon, Kim Yutai
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
# You are responsible for all liability arising out of the abuse of this program.
# This program is available to everyone, including businesses.
# Use for commerical purposes is restricted.


import os
import smtplib
import time
import netifaces
import getpass
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# mail server setting
MAIL_SERVER = "smtp.naver.com"
MAIL_SERVER_PORT = 465

input_mail_account_msg = """
##############################################
Step 1. Set up sender's mail account
##############################################

Enter the sender's mail account and password

Note 1: The information you enter is not stored anywhere. Do not worry
Note 2: When using naver mail, you need to set up smtp in advance.
"""

select_emailtext_msg =  """
##############################################
Step 2. Choose a mail subject
##############################################

Please select the subject of your mail to be sent
The body of the message can be found in the webdir directory.
"""

input_server_name_msg = """ 
##############################################
Step 3. Set server address
##############################################

Please enter a domain address or ip address.
If no value is entered, it is set to the current address.

ex)
10.10.10.10
10.10.10.10:8000
www.mailtraining.com
www.mailtraining.com:8000

"""


input_email_msg = """
##############################################
Step 4. Set recipient mail address
##############################################

Please enter email address of users.
Each line is separated by "Enter key".
If you want to quit to input your email list, please push "enter key" again.

ex) 
aaa@email.com
bbb@email.com
ccc@email.com

type here==>
""" 

def SendMail(mail_id, mail_pwd, reciever, subject, mailbody):

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = mail_id 
	msg['To'] = reciever 

	part1 = MIMEText(mailbody, 'html')

	msg.attach(part1)

	mail = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_SERVER_PORT)
	mail.ehlo()
	#mail.starttls()
	mail.login(mail_id, mail_pwd)
	mail.sendmail(mail_id, reciever, msg.as_string())
	mail.quit()
	print("send mail to %s "%reciever)
	

def InputMessage():
	os.system("clear")
	text = ""
	stopword = ""

	print(input_email_msg)
	
	while True:
		line = input()
		if line.strip() == stopword:
			if len(text) == 0:
				print("email list is empty!!")
				print("type email list!!\n\n")
				print("==>")
				continue

			break
		text += "%s\n" % line

	return text


def GetMailText(mail_index):
	with open("./webdir/%s/subject.txt"%mail_index, "r") as text_file:
		subject = text_file.read()
	with open("./webdir/%s//body.txt"%mail_index, "r") as text_file:
		mailbody= text_file.read()
	return subject, mailbody


def SelectEmailText():
	os.system("clear")
	print(select_emailtext_msg)
	print("Email Subject List:")
	dirlist = os.listdir("./webdir")
	dirlist.reverse()

	for index in dirlist:
		with open("./webdir/%s/subject.txt"%index, "r") as text_file:
			subject = text_file.read().strip()
		print("%s : %s"%(index,subject))

	
	while True:
		print("")
		line = input("type number==>  ")

		if line in dirlist:
			break
		
		else:
			print("invalid index number! try again:")
			continue
			

	return line

def get_mail_account():
	print(input_mail_account_msg)
	mail_id = input("mail id: ")
	mail_pwd = getpass.getpass("mail password: ")
	return mail_id, mail_pwd
	

def get_server_name(mail_index):
	os.system("clear")
	print(input_server_name_msg)

	servername = netifaces.ifaddresses('enp0s3')[netifaces.AF_INET][0]['addr']
	print("Current server address is  [ %s ]"%servername)

	while True:
		print("")
		print("")
		tmp = input("type here ==> ")
		if tmp == "":
			tmp = servername

		print("\n\nyour input : %s"%tmp)
		print("Generated URL : http://%s/login/%s/login.php"%(tmp,mail_index))
		os.system("firefox http://%s/login/%s/login.php"%(tmp,mail_index))

		print("\n")
		check = input("Does the URL look right? (Y/n)")

		if check.lower() == "y":
			servername = tmp
			break

	
	return servername

def process_mailbody(mailbody, reciever, servername, mail_index):
	mailbody = mailbody.replace("<emailaddress>", reciever)
	mailbody = mailbody.replace("<username>", reciever.split('@')[0])
	mailbody = mailbody.replace("<mailindex>", mail_index)
	mailbody = mailbody.replace("<serveraddress>", servername)
	mailbody = mailbody.replace("<mailserverdomain>", reciever.split('@')[-1])
	
	return mailbody
	
if __name__== "__main__":
	os.system("clear")
	mail_id,mail_pwd = get_mail_account()
	mail_index = SelectEmailText()
	servername = get_server_name(mail_index)
	subject, mailbody = GetMailText(mail_index)
	result = InputMessage()

	os.system("clear")
	print("Start sending mail......\n\n")
	for reciever in result.splitlines():
		result_mailbody = process_mailbody(mailbody, reciever, servername, mail_index)
		SendMail(mail_id, mail_pwd, reciever, subject, result_mailbody)

	time.sleep(20)

#!/usr/bin/env python
########################################################################
# Use Python 3 and IMAP to iterate over emails in the Inbox
#
# HISTORICAL INFORMATION -
#
#  2017-06-21  msipin  Attempted to handle "bad SUBJECT lines".
########################################################################
import sys
import imaplib
import getpass
import email
import email.header
import datetime


# DEAR GOD IN HEAVEN, DON'T GIVE ANYONE THIS FILE WITHOUT
# CHANGING THE FOLLOWING THREE LINES TO SOMETHING BENIGN -
EMAIL_SERVER="this.should.be.the.fqdn.of.your.email.server"
EMAIL_ACCOUNT = "your_user_name@your_domain_name.com"
EMAIL_PASS="YourPasswordHere"


# Folder to read (Usually use 'Inbox')
EMAIL_FOLDER = "Inbox"


def process_mailbox(M,filter):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """
    rv, data = M.search(None, filter)
    if rv != 'OK':
        print("No messages found!")
        return

    num_msgs=0
    for num in data[0].split():
        num_msgs=num_msgs+1
    if (num_msgs == 1): print("You have {0} message".format(num_msgs))
    else: print("You have {0} messages".format(num_msgs))

    for num in data[0].split():
        #rv, data = M.fetch(num, '(RFC822)')
        rv, data = M.fetch(num, '(BODY.PEEK[HEADER])')
        if rv != 'OK':
            print("ERROR 'peeking' at message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        try:
            hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
            subject = str(hdr)
        except TypeError:
            subject = "(unknown)"
        print('\nMessage # %d - Subj: %s' % (int(num), subject))
        #print('Raw Date:', msg['Date'])
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print ("        Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S"))


########################## Start of (anonymous) program ##########################
M = imaplib.IMAP4_SSL(EMAIL_SERVER)

filter="ALL"		# Everything in the current folder

if len(sys.argv)>1 and sys.argv[1] == "all":
    filter = "ALL"
elif len(sys.argv)>1 and sys.argv[1] == "new":
    filter = "UNSEEN"
elif len(sys.argv)>1:
    filter = '(SUBJECT "'
    for i in range(1,len(sys.argv)):
        if (i>1): filter += " "
        filter += sys.argv[i]
    filter += '")'
#print("Filter = [{0}]", filter)

try:
    ##rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
    rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASS)
except imaplib.IMAP4.error:
    print ("LOGIN FAILED!!! ")
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    print("Mailboxes:")
    print(mailboxes)

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print("Processing mailbox...\n")
    process_mailbox(M, filter)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()

print ("\n")

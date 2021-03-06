#!/usr/bin/env python3
########################################################################
# Use Python 3 and IMAP to iterate over emails in the Inbox
#
# HISTORICAL INFORMATION -
#
#  2017-06-21  msipin  Attempted to handle "bad SUBJECT lines".
#  2017-06-29  msipin  Moved email credentials to external file named
#                      "email_creds.py" (which git is set to ignore)
#  2017-07-02  msipin  Allowed user to specify which account they want
#                      to use from the (new) email_creds.conf file.
#  2019-08-22  msipin  Added ability to skip displaying the subject line
#                      for each message by adding the "-c" (count) command
#                      line flag.
#  2020-06-11  msipin  Added help function and some error checking. Turned all
#                      hard-coded command-line arguments into variables.
########################################################################
import sys
import imaplib
import getpass
import email
import email.header
import datetime


try:
    import configparser
except ImportError:
    print("\nERROR: Can't find 'configparser'.  Try performing 'sudo pip3 install ConfigParser'\n")
    sys.exit(-1)


ARG_ACCOUNT="-a"	# Argument to specify which email ACCOUNT to use
ARG_COUNT="-c"	# COUNT, only
ARG_ALL="all"
ARG_NEW="new"
ARG_HELP="-h"

def help():
	print("")
	print("usage: %s [ %s | %s <account> | %s | %s | %s ]\n" % (sys.argv[0],ARG_HELP,ARG_ACCOUNT,ARG_COUNT,ARG_ALL,ARG_NEW))

# end of help()



# Folder to read (Usually use 'Inbox')
EMAIL_FOLDER = "Inbox"


def process_mailbox(M,filter,showEach):
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

    if showEach:
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

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1



########################## Start of (anonymous) program ##########################

# If user does not specify which account, the default
# account will be used, and the argBase value should
# be set to "argument 1"
argBase=1

# Default to showing the subject lines for every email retrieved
showAll=True

############## DEFINE EMAIL CREDS (and from what account) ############## 
Config = configparser.ConfigParser()
Config.read("email_creds.conf")
#print(Config.sections())

# If user wants to see command help -
if (len(sys.argv)>argBase and ARG_HELP == sys.argv[argBase]):
        help()
        sys.exit(-2)
    # endif

# If user specified an account, pick it up
if (len(sys.argv)>argBase and ARG_ACCOUNT == sys.argv[argBase]):
    #print("DEBUG: argBase: ",argBase," len(sys.argv): ",len(sys.argv))
    if (argBase+1 >= len(sys.argv)):
        print("\nError: No account specified!")
        help()
        sys.exit(-1)
    # endif

    # User wants to override default
    # so pick it up!
    acct=sys.argv[argBase+1]

    # Advance the argument base beyond both the
    # command-line-argument flag and its parameter
    argBase += 2

else:
    # Figure out what the default account is
    acct=ConfigSectionMap("default")['account']

#print("DEBUG: Account = [{0}]".format(acct))


# Check if user just wants a count
if (len(sys.argv)>argBase and ARG_COUNT == sys.argv[argBase]):
    # User JUST wants a count (aka don't display them!)
    showAll=False

    # Advance the argument base beyond the command-line-argument flag
    argBase += 1



# Establish email server + credentials...
EMAIL_SERVER="undefined"
EMAIL_ACCOUNT="undefined"
EMAIL_PASS="undefined"

try:
    try:
        EMAIL_SERVER=ConfigSectionMap(acct)['email_server_imap']
    except KeyError:
        print("\nERROR: No value for [{0}][email_server_imap] in config file\n".format(acct))
        sys.exit(-1)
    try:
        EMAIL_ACCOUNT=ConfigSectionMap(acct)['email_account']
    except KeyError:
        print("\nERROR: No value for [{0}][email_account] in config file\n".format(acct))
        sys.exit(-1)
    try:
        EMAIL_PASS=ConfigSectionMap(acct)['email_pass']
    except KeyError:
        print("\nERROR: No value for [{0}][email_pass] in config file\n".format(acct))
        sys.exit(-1)
except configparser.NoSectionError:
    print("\nERROR: No account called [{0}] in config file\n".format(acct))
    sys.exit(-1)

#print("DEBUG: EMAIL_SERVER=[{0}]".format(EMAIL_SERVER))
#print("DEBUG: EMAIL_ACCOUNT=[{0}]".format(EMAIL_ACCOUNT))
#print("DEBUG: EMAIL_PASS=[{0}]".format(EMAIL_PASS))

sys.exit(2)


M = imaplib.IMAP4_SSL(EMAIL_SERVER)

filter="ALL"		# Everything in the current folder



if len(sys.argv)>argBase and sys.argv[argBase] == ARG_ALL:
    filter = "ALL"
elif len(sys.argv)>argBase and sys.argv[argBase] == ARG_NEW:
    filter = "UNSEEN"
elif len(sys.argv)>argBase:
    filter = '(SUBJECT "'
    for i in range(argBase,len(sys.argv)):
        if (i>argBase): filter += " "
        filter += sys.argv[i]
    filter += '")'
##print("Filter = [{0}]", filter)

try:
    ##rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
    rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASS)
except imaplib.IMAP4.error:
    print ("EMAIL LOGIN FAILED!")
    sys.exit(1)

##print(rv, data)

rv, mailboxes = M.list()
#if rv == 'OK':
#    print("Mailboxes:")
#    print(mailboxes)

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    # print("Processing mailbox...\n")
    process_mailbox(M, filter, showAll)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()

#print ("\n")


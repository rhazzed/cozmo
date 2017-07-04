#!/usr/bin/env python3
############################################################
# smtp_python3.py - Send EMAIL via SMTP.
#
# HISTORICAL INFORMATION -
#
#  2017-07-03  msipin  Created.
#                      Added ability to specify subject using
#                      the "-s" command-line argument.
############################################################

####################3
# EXAMPLE USAGE -
#   smtp_python3.py eric@whatever.com "This text here will be in the body of the email."
#   smtp_python3.py -a yahoo eric@whatever.com "This text here will be in the body of the email."
#   smtp_python3.py -a yahoo -s "This is the Subject" eric@whatever.com "This is the body of the email."
#   smtp_python3.py eric@whatever.com A b c d e f g the_end
#   smtp_python3.py -a gmail mike@youknowit.com `cat message.txt`
#     -- where "message.txt" is a text file contining the
#        body (text) of a messge to send in the email
####################3

from smtplib import SMTP_SSL as SMTP
import logging
import logging.handlers
import sys
from email.mime.text import MIMEText

try:
    import configparser
except ImportError:
    print("\nERROR: Can't find 'configparser'.  Try performing 'sudo pip3 install ConfigParser'\n")
    sys.exit(-1)



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



# If user does not specify which account, the default
# account will be used, and the argBase value should
# be set to "argument 1"
argBase=1

############## DEFINE EMAIL CREDS (and from what account) ############## 
Config = configparser.ConfigParser()
Config.read("email_creds.conf")
#print(Config.sections())

# If user specified an account, pick it up
if (len(sys.argv)>2 and "-a" == sys.argv[1]):
    # User wants to override default
    # so pick it up!
    acct=sys.argv[2]

    # Advance the argument base beyond both the
    # command-line-argument flag and its parameter
    argBase += 2

else:
    # Figure out what the default account is
    acct=ConfigSectionMap("default")['account']

#print("DEBUG: Account = [{0}]".format(acct))

# Establish the "default email subject"
msg_subject = "Cozmo Email via BSE" 

# If user specified an email Subject line, pick it up
if (len(sys.argv)>(argBase+2) and "-s" == sys.argv[argBase]):
    # User wants to override default
    # so pick it up!
    msg_subject=sys.argv[argBase+1]

    # Advance the argument base beyond both the
    # command-line-argument flag and its parameter
    argBase += 2


#print("DEBUG: Subject = [{0}]".format(msg_subject))




# Establish email server + credentials...
EMAIL_SERVER="undefined"
EMAIL_ACCOUNT="undefined"
EMAIL_PASS="undefined"

try:
    try:
        EMAIL_SERVER=ConfigSectionMap(acct)['email_server_smtp']
    except KeyError:
        print("\nERROR: No value for [{0}][email_server_smtp] in config file\n".format(acct))
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




if (len(sys.argv) < (argBase + 2)) or not ("@" in sys.argv[argBase]):
    sys.stderr.write('\nusage: {0} <to@example.com> <message text goes here...>\n\n'.format(sys.argv[0]))
    sys.exit(1)


to_email = sys.argv[argBase]
#print("DEBUG: EMAIL_TO=[{0}]".format(to_email))

text = ''
for i in range(argBase+1,len(sys.argv)):
    if (i > (argBase+1)):
        text += ' '
    text += sys.argv[i]

msg = MIMEText(text, 'plain')
msg['Subject'] = msg_subject
from_email = EMAIL_ACCOUNT
msg['To'] = to_email

#print("DEBUG: EMAIL_TEXT=[{0}]".format(text))


msg['From'] = from_email
try:
    conn = SMTP(EMAIL_SERVER)
    conn.set_debuglevel(True)
    conn.login(EMAIL_ACCOUNT, EMAIL_PASS)
    try:
        conn.sendmail(from_email, to_email, msg.as_string())
    finally:
        conn.close()

except Exception as exc:
    sys.exit("Mail failed: {}".format(exc))


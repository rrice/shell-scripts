#!/usr/bin/env python

#
# -*- mode: Python; fill-column: 75; -*-
#
# Copyright (c) 2017 Ralph Allan Rice <ralph.rice@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys, argparse, smtplib, email

parser = argparse.ArgumentParser(prog='gmail-send', description='Sent a MIME message via Gmail.')
parser.add_argument('--from', dest='from_addr', help='the sender email address.', required=True )
parser.add_argument('--to', dest='to_addr', help='the receiver email address.', required=True)
parser.add_argument('--user', dest='user', help='the SMTP account user name.', required=True)
parser.add_argument('--password', dest='password', help='the SMTP account password', required=True)
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='the MIME message file to send.  If not provided, the message will be taken from standard input.')

args = parser.parse_args()
smtp_host = "smtp.gmail.com"
smtp_port = 587

data = args.file.read()

args.file.close()

message = email.message_from_string(data)

message.replace_header("From", args.from_addr)
message.replace_header("To", args.to_addr)

smtp = smtplib.SMTP(smtp_host, smtp_port)
smtp.ehlo()
smtp.starttls()
smtp.login(args.user, args.password)
smtp.sendmail(args.from_addr, args.to_addr, message.as_string())
smtp.quit()


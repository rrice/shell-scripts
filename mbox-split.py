#!/usr/bin/env python3
#
# -*- mode: python; fill-column: 75; comment-column: 50; -*-
#
# Copyright (c) 2013 Ralph Allan Rice <ralph.rice@gmail.com>
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

import argparse
import os
import mailbox
import email
from email.generator import BytesGenerator
import uuid

# Constants
name_keys = ['subject', 'message-id', 'content-id']


def parse_command_line():
    """
    Parse the command line.
    """
    cmdline = argparse.ArgumentParser(
        description='Split messages contained in an mbox ' +
        'into separate files.')
    cmdline.add_argument('mbox', help='the mbox file to read.')
    cmdline.add_argument('-d', '--output-dir', 
                     dest='dir', 
                     help='the directory to output the message files.', 
                     default=os.getcwd())
    return cmdline.parse_args()

def pick_first_value(message, keys):
    """ 
    Pick the first message value that is not None
    from the set of keys.
    """
    for key in keys:
        if not message[key] is None:
            return message[key]
    return uuid.UUID().hex

def write_message_to_file(message, filename):
    """
    Write a message to the file with the
    given filename.
    """
    fp = open(os.path.join(args.dir, filename), 'wb')
    try:
        generator = BytesGenerator(fp)
        generator.flatten(message, linesep='\r\n')
    finally:
        fp.close()



args = parse_command_line()
inbox = mailbox.mbox(args.mbox)

for message in inbox:
    basename = pick_first_value(message, name_keys)
    filename = '-'.join(basename.lower().split()) +'.eml'
    write_message_to_file(message, filename)

    

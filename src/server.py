#! /usr/bin/env python3

# File Transfer server program

import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import params
from archiver import *

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "ftServer"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

file = "one"

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)

        if os.path.exists(file):

            archived_msg = send_msg(file)

            while len(archived_msg):
                bytesSent = conn.send(archived_msg)
                archived_msg = archived_msg[bytesSent:0]
                receive_msg("test.txt", archived_msg)

            time.sleep(0.25)       # delay 1/4s
            conn.shutdown(socket.SHUT_WR)
            sys.exit(0)


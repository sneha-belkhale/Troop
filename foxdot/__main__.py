"""
    FoxDot __main__.py
    ------------------

    Use FoxDot's interface by running this as a Python script, e.g.
    python __main__.py or python -m FoxDot if you have FoxDot correctly
    installed and Python on your path.

"""

from __future__ import absolute_import, division, print_function
from .lib import FoxDotCode, handle_stdin, handle_string
from .lib.Workspace import workspace
import sys
import socket

# If we are getting command line input

if sys.argv[-1] == "--pipe":

    # Set up pipe

    handle_stdin()

if sys.argv[-1] == "--socket":

    # Set up socket and listen for connections

    host = "0.0.0.0"
    port = 54321

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print ("from connected  user: " + str(data))
        data = str(data)
        response = handle_string(data);
        print("sending: " + response)
        conn.send(response.encode())
    conn.close()

else:

    # Start the gui

    FoxDot = workspace(FoxDotCode).run()

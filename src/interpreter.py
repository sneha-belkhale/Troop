"""
    Interpreter
    -----------

    Runs a block of FoxDot code. Designed to be overloaded
    for other language communication

"""
from __future__ import absolute_import
from .config import *

from subprocess import Popen
from subprocess import PIPE, STDOUT
from datetime import datetime

import socket
# Import OSC library depending on Python version

if PY_VERSION == 2:
    from . import OSC
else:
    from . import OSC3 as OSC

try:
    broken_pipe_exception = BrokenPipeError
except NameError:  # Python 2
    broken_pipe_exception = IOError

import sys
import re
import time
import threading
import shlex

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

def compile_regex(kw):
    """ Takes a list of strings and returns a regex that
        matches each one """
    return re.compile(r"(?<![a-zA-Z.])(" + "|".join(kw) + ")(?![a-zA-Z])")

SEPARATOR = ":"; _ = " %s " % SEPARATOR

def colour_format(text, colour):
    return '<colour="{}">{}</colour>'.format(colour, text)

## dummy interpreter

class DummyInterpreter:
    def __init__(self, *args, **kwargs):
        self.re={}

    def __repr__(self):
        return repr(self.__class__.__name__)

    def get_block_of_code(self, text, index):
        """ Returns the start and end line numbers of the text to evaluate when pressing Ctrl+Return. """

        # Get start and end of the buffer
        start, end = "1.0", text.index("end")
        lastline   = int(end.split('.')[0]) + 1

        # Indicies of block to execute
        block = [0,0]

        # 1. Get position of cursor
        cur_x, cur_y = index.split(".")
        cur_x, cur_y = int(cur_x), int(cur_y)

        # 2. Go through line by line (back) and see what it's value is

        for line in range(cur_x, 0, -1):
            if not text.get("%d.0" % line, "%d.end" % line).strip():
                break

        block[0] = line

        # 3. Iterate forwards until we get two \n\n or index==END
        for line in range(cur_x, lastline):
            if not text.get("%d.0" % line, "%d.end" % line).strip():
                break

        block[1] = line

        return block

    def evaluate(self, string, *args, **kwargs):
        self.print_stdin(string, *args, **kwargs)
        return

    def start(self):
        return self

    def stdout(self, *args, **kwargs):
        pass

    def kill(self, *args, **kwargs):
        pass

    def print_stdin(self, string, name=None, colour="White"):
        """ Handles the printing of the execute code to screen with coloured
            names and formatting """
        # Split on newlines
        string = [line.replace("\n", "") for line in string.split("\n") if len(line.strip()) > 0]
        if len(string) > 0 and name is not None:
            name = str(name)
            print(colour_format(name, colour) + _ + string[0])
            # Use ... for the remainder  of the  lines
            n = len(name)
            for i in range(1,len(string)):
                sys.stdout.write(colour_format("." * n, colour) + _ + string[i])
                sys.stdout.flush()
        return

    def stop_sound(self):
        """ Returns the string for stopping all sound in a language """
        return ""

    @staticmethod
    def format(string):
        """ Method to be overloaded in sub-classes for formatting strings to be evaluated """
        return string

class Interpreter(DummyInterpreter):
    lang     = None
    clock    = None
    keyword_regex = compile_regex([])
    comment_regex = compile_regex([])
    stdout   = None
    stdout_thread = None
    filetype = ".txt"
    def __init__(self, path):

        self.re = {"tag_bold": self.find_keyword, "tag_italic": self.find_comment}

        if exe_exists(path.split()[0]):

            self.path = path

        else:

            raise ExecutableNotFoundError("'{}' is not a valid executable. Using Dummy Interpreter instead.".format(path))

        import tempfile

        self.f_out = tempfile.TemporaryFile("w+", 1) # buffering = 1
        self.is_alive = False
        self.alive = False

    def start(self):
        # """ Opens the process with the interpreter language """
        # self.lang = Popen(shlex.split(self.path), shell=False, universal_newlines=True, bufsize=1,
        #                   stdin=PIPE,
        #                   stdout=self.f_out,
        #                   stderr=self.f_out)
        """ Opens a socket for FoxDot only!! """
        self.mySocket = socket.socket()
        self.mySocket.connect(('localhost', 54321))
        self.alive = True;
        self.stdout_thread = threading.Thread(target=self.stdout)
        self.stdout_thread.start()
        self.is_alive = True;
        return self

    def find_keyword(self, string):
        return [(match.start(), match.end()) for match in self.keyword_regex.finditer(string)]

    def find_comment(self, string):
        return [(match.start(), match.end()) for match in self.comment_regex.finditer(string)]

    def write_socket(self, string):
        self.mySocket.send(string.encode())
        return

    def evaluate(self, string, *args, **kwargs):
        """ Sends a string to the stdin and prints the text to the console """
        # Print to console
        self.print_stdin(string, *args, **kwargs)
        # Write to the socket
        self.write_socket(string)
        return

    def stdout(self, text=""):
        while True:
            if self.alive:
                data = self.mySocket.recv(1024).decode()
                if not data:
                    break
                print(data)


        # """ Continually reads the stdout from the self.lang process """
        # while self.is_alive:
        #     if self.lang.poll():
        #         self.is_alive = False
        #         break
        #     try:
        #         # Check contents of file
        #         self.f_out.seek(0)
        #         for stdout_line in iter(self.f_out.readline, ""):
        #             sys.stdout.write(stdout_line.rstrip())
        #         # clear tmpfile
        #         self.f_out.truncate(0)
        #         time.sleep(0.05)
        #     except ValueError as e:
        #         print(e)
        #         return
        return

    def kill(self):
        """ Stops communicating with the subprocess """
        # End process if not done so already
        self.is_alive = False
        if self.lang.poll() is None:
            self.lang.communicate()

class FoxDotInterpreter(Interpreter):
    filetype=".py"
    path = "docker run -t publictrooper /bin/bash"

    def __init__(self):

        Interpreter.__init__(self, self.path)

        self.keywords = ["Clock", "Scale", "Root", "var", "linvar", '>>']

        self.keyword_regex = compile_regex(self.keywords)

    def __repr__(self):
        return "FoxDot"

    @staticmethod
    def format(string):
        return "{}\n\n".format(string)

    @classmethod
    def find_comment(cls, string):
        instring, instring_char = False, ""
        for i, char in enumerate(string):
            if char in ('"', "'"):
                if instring:
                    if char == instring_char:
                        instring = False
                        instring_char = ""
                else:
                    instring = True
                    instring_char = char
            elif char == "#":
              if not instring:
                  return [(i, len(string))]
        return []

    def kill(self):
        self.evaluate(self.stop_sound())
        Interpreter.kill(self)
        return

    def stop_sound(self):
        return "Clock.clear()"


langtypes = { FOXDOT        : FoxDotInterpreter}

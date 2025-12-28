#!/usr/bin/python3
"a simple wrapper around the frotz engine"
import datetime
import inspect
import logging
import os
import sys
import subprocess
import time

class Zork:
    "wraps a z-engine"
    FROTZ = "dfrotz" # dumb frotz, should be somewhere in the PATH
    FROTZ_OPTIONS = [
        "-m", # no 'more' prompt
        "-p", # ASCII only
        "-q", # quiet mode, no startup messages
        "-w", "255" # max number
    ]
    ZORK = "zork1.dat" # should be in the same PATH
    PROMPT = b'>'
    LOGFILE = "zork.log"
    LOGPREFIX = "\n  "

    def __init__(self, do_log = True):
        "initialization, instantiates the z-machine, starts logging"
        if do_log:
            logging.basicConfig(filename = self.LOGFILE,
                                filemode = 'w',
                                format='%(asctime)s %(message)s',
                                level = logging.DEBUG)
        else:
            logging.disable(logging.CRITICAL)
        self._frotz = None
        self._last = [] # last result
        self._reset_engine()

    def __del__(self):
        "the 'destructor'"
        self.quit()

    def _read(self, prompt=None):
        "reads until prompt, return as lines"
        time.sleep(0.02) # wait a little
        char = b' '
        output = b''
        if prompt is None:
            prompt = self.PROMPT            
        while char != prompt:
            char = self._frotz.stdout.read(1)
            output += char
        lines = [line.strip() for line in output.split(b'\n')]
        lines = [line.decode("ASCII") for line in lines if line]
        self._dodebug(*lines)
        return lines

    def _dodebug(self, *msg):
        "log a debug message with info from where it was called"
        call_name = inspect.stack()[1][3]
        lineno = inspect.stack()[1][2]
        tolog = f"{call_name} ({lineno}):"
        toadd = self.LOGPREFIX.join(map(str, msg))
        if toadd:
            tolog += self.LOGPREFIX + toadd
        logging.debug(tolog)

    def _write(self, command):
        "send a command to the frotz engine"
        self._dodebug(command)
        command += "\n" # do it
        raw_command = command.encode()
        self._frotz.stdin.write(raw_command)
        self._frotz.stdin.flush() # ensure it is done

    def _reset_engine(self):
        "initialize (resets) the engine"
        if self._frotz is not None:
            self.quit()
            self._frotz = None
        engine_command = [self.FROTZ]
        engine_command.extend(self.FROTZ_OPTIONS)
        engine_command.append(self.ZORK)
        msg = "starting engine with"
        self._dodebug(msg, " ".join(engine_command))
        self._frotz = subprocess.Popen(engine_command,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        time.sleep(0.2) # wait a little to power up the z-machine
        intro = self._read()
        if not intro or not intro[0].startswith("ZORK I"):
            logging.error("_reset_engine: Did not start with ZORK I")
            self._frotz = None
            self._last = []
            raise ValueError("is that Zork?")
        info = intro[4:-1] # remove statement and prompt
        self._last = info[:]
        self._dodebug(*info)
        return info

    def command(self, cmd, prompt=None):
        "send an arbitrary string, receive the result of the command"
        if not isinstance(cmd, list) and not isinstance(cmd, tuple):
            cmd = [str(cmd)] # handle single strings
        parts = []
        for part in cmd:
            if not isinstance(part, str):
                part = " ".join(str(p).strip() for p in part)
            else:
                part = part.strip()
            parts.append(part)
        cmd = " ".join(parts)
        self._write(cmd)
        result = self._read(prompt)
        result = result[:-1] # remove prompt
        self._last = result[:]
        return result

    @property
    def last(self):
        "the result of the last command"
        return self._last

    def save(self, filename=None):
        "save the current state to a file"
        if filename is None:
            sdt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"zork{sdt}.dat"
        if os.path.isfile(filename):
            os.remove(filename)
        self.command("save", b':')
        self.command(filename)

    def load(self, filename):
        "load the current state from a file"
        if filename is None or not os.path.isfile(filename):
            raise ValueError("file " + filename + " does not exist")
        self.command("restore", b':')
        self.command(filename)

    restore = load
    
    def quit(self):
        self._last = []
        if self._frotz:
            self._frotz.stdin.close()
            self._frotz = None

    def reset(self):
        self.quit()
        self._reset_engine()
            
def test(args):
    "test"
    debug = False if args and args[0][0] == "s" else True # silent
    zork = Zork(debug)
    def show_result(result = None):
        if not result:
            result = zork.last
        print("  " + "\n  ".join(result))
    show_result()
    doit = ["open mailbox",
            ("read", "leaflet"), # can do list/tuple of strings
            "inventory",
            "look",
            "go south",
            "go east",
            "open window",
            "enter house",
            "take bottle",
            "look",
            "inventory",
            ]
    for doing in doit:
        print(doing)
        result = zork.command(doing)
        show_result(result)
    zork.save("zorka.save")
    zork.reset()
    print("reset, inventory")
    result = zork.command("inventory")
    show_result(result)
    print("restore, inventory")
    zork.restore("zorka.save")
    result = zork.command("inventory")
    show_result(result)    
    print("done")

if __name__ == '__main__':
    test(sys.argv[1:])

import sys
import getopt
import os
import subprocess
import json

"""
A class used to extract the Install Path of some programs on windows

...

Attributes
----------
name : str
    the name of the executeable program, e.g. yarn.cmd
"""

stderr = ""
stdout = ""


def print_help(fname):
    """ just a simple help output """
    print("%s -n, --name <name of executeable>" % fname)


def main(argv):
    fname = os.path.basename(__file__)
    search_name = ""
    try:
        # argv, shortopts, longopts
        # : requires an argument
        opts, args = getopt.getopt(argv, "hn:", ["name="])
    except getopt.GetoptError:
        print_help(fname)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help(fname)
            sys.exit()
        elif opt in ("-n", "--name"):
            search_name = arg
            doTheJob(search_name)

    print_help(fname)
    sys.exit()


def runCmd(cmd):
    ''' runs a command '''
    global stderr, stdout
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            bufsize=0,
                            preexec_fn=None)
    for line in iter(proc.stderr.readline, b''):
        stderr += line.decode()

    for line in iter(proc.stdout.readline, b''):
        stdout += line.decode()
    proc.communicate()

    return stdout.replace("\r\n", "")


def doTheJob(name):
    global json
    """ Search on the system for name """
    # print("Searching for %s" % name)
    cmd = "where.exe %s" % name
    output = runCmd(cmd)

    data = {
        "response": output
    }
    print(json.dumps(data))
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])

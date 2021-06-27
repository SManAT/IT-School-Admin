import sys
import getopt
import os
import json
from pathlib import Path

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
    print(json.dumps({
        "failed": True,
        "msg": "No arguments provided!"
    }))
    sys.exit(1)


def searchFile(name):
    locations = [
        os.environ["APPDATA"],
        os.environ["ProgramFiles"],
        os.environ["ProgramFiles(x86)"]
        os.environ["LOCALAPPDATA"],
    ]
    exclude = ["Temp\\", "npm\\node_modules\\"]
    abort = False
    for p in locations:
        if abort is True:
            break
        for root, dirs, files in os.walk(p):
            # exclude some patterns
            direxcluded = False
            for test in exclude:
                if test.lower() in root.lower():
                    direxcluded = True
            if direxcluded is False:
                for file in files:
                    if file.lower() == name.lower():
                        ffound = os.path.join(root, str(file))
                        abort = True
                        break
    return ffound


def doTheJob(name):
    global json
    """ Search on the system for name """
    output = searchFile(name)

    data = {
        "response": output
    }
    print(json.dumps(data))
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])

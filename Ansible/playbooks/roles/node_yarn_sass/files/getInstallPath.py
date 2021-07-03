import sys
import argparse
import os
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


def main():
    # see https://www.golinuxcloud.com/python-argparse/
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name',
                        dest='search_name',
                        help='The name of the File to be searched',
                        type=str,
                        required=True
                        )
    args = parser.parse_args()
    doTheJob(args.search_name)


def searchFile(name):
    locations = [
        os.environ["APPDATA"],
        os.environ["ProgramFiles"],
        os.environ["ProgramFiles(x86)"],
        os.environ["LOCALAPPDATA"]
    ]
    exclude = ["Temp\\", "node_modules\\"]
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
    # just the path
    return os.path.dirname(ffound)


def doTheJob(name):
    """ Search on the system for name """
    output = searchFile(name)

    data = {
        "response": output
    }
    print(json.dumps(data))
    sys.exit()


if __name__ == "__main__":
    main()

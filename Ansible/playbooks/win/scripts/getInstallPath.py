import sys
import getopt
import os

"""
    A class used to extract the Install Path of some programs on windows

    ...

    Attributes
    ----------
    name : str
        the name of the executeable program, e.g. yarn.cmd
    """


def print_help(fname):
    """ just a simple help output """
    print("%s -name <name of executeable>" % fname)


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
    print("Searching for %s" % search_name)


if __name__ == "__main__":
    main(sys.argv[1:])

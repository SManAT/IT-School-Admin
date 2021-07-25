import uuid
import re


class MySQL:
    """ load MAC Adress and get Hostname from MySQL DB """

    def __init__(self):
        self.getMacAdresses()

    def getHostData(self):
        self.getMacAdresses()

    def getMacAdresses(self):
        """ get MAC Adresses of eths """
        print(uuid.getnode())

        print("The MAC address in expressed in formatted and less complex way : ", end="")
        print(':'.join(re.findall('..', '%012x' % uuid.getnode())))

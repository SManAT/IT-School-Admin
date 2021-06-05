class User():
    """ Data Wrapper """
    def __init__(self):
        self.username = ""
        self.hosts = ""
        self.pwd = ""
        self.privileges = []

    def get_username(self):
        return self.__username


    def get_hosts(self):
        return self.__hosts


    def get_pwd(self):
        return self.__pwd


    def set_username(self, value):
        self.__username = value


    def set_hosts(self, value):
        self.__hosts = value


    def set_pwd(self, value):
        self.__pwd = value
        
    def add_privilege(self, value):
        self.privileges.append(value)
        
    def get_privileges(self):
        return self.privileges
    
    def set_privileges(self, value):
        self.privileges = value
    
    def print_privileges(self):
        for line in self.privileges:
            print(line)

        
    def __str__(self):
        msg = "Username: %s\nHosts: %s\nPwd: %s\n" % (self.get_username(), self.get_hosts(), self.get_pwd())
        msg += "Privilegs:\n"
        for p in self.get_privileges():
            msg += p+"\n"
                                    
        return msg

    
    
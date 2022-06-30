import subprocess


class CmdRunner():
    """ A Class for runing cmds with subprocess """

    def __init__(self):
        self._stderr = ""
        self._stdout = ""

    def getStderr(self):
        return self._stderr

    def getStdout(self):
        return self._stdout

    def getLines(self):
        ''' give me an array of lines from stdout '''
        # split the text
        words = self._stdout.split("\n")
        return words

    def runCmd(self, cmd):
        ''' runs a command '''
        self._stderr = ""
        self._stdout = ""
        signedCmd = 'Powershell.exe -command "%s"' % cmd
        # print(signedCmd)
        proc = subprocess.Popen(signedCmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                bufsize=0,
                                preexec_fn=None)
        for line in iter(proc.stderr.readline, b''):
            self._stderr += line.decode()

        for line in iter(proc.stdout.readline, b''):
            self._stdout += line.decode()
        proc.communicate()

        self.pid = proc.pid

    def getPID(self):
        """ returns the running PID """
        return self.pid

    def runPSFile(self, filename):
        """ runs a PS File """
        self._stderr = ""
        self._stdout = ""

        signedCmd = 'Powershell.exe -File "%s"' % filename
        proc = subprocess.Popen(signedCmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                bufsize=0,
                                preexec_fn=None)
        for line in iter(proc.stderr.readline, b''):
            self._stderr += line.decode('utf-8', 'ignore')

        for line in iter(proc.stdout.readline, b''):
            self._stdout += line.decode('utf-8', 'ignore')
        proc.communicate()

        self.pid = proc.pid

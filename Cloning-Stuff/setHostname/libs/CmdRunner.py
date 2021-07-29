import subprocess
from subprocess import CREATE_NEW_CONSOLE
import sys
import os


class CmdRunner():
    ''' A Class for runing cmds with subprocess, also as a specific user '''
    pid = None

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

        proc = subprocess.Popen(cmd,
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

    def runPSFile(self, filename):
        cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File %s" % filename
        print(cmd)
        os.system(cmd)
        """
        ''' runs a PS File '''
        self._stderr = ""
        self._stdout = ""

        proc = subprocess.Popen(["powershell.exe", '-ExecutionPolicy', 'RemoteSigned', filename],
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        (output, err) = proc.communicate()
        self._stderr = err
        self._stdout = output
        
        # This makes the wait possible
        proc.wait()

        self.pid = proc.pid
        """
        
    def runPSCommand(self, cmd):
        """ runs a PS Command """
        completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        return completed

    def getPID(self):
        """ returns the running PID """
        return self.pid

import os
import logging
import sys
from pathlib import Path


class Tools:
    """ Stuff to Scripts, Filemanagement """

    def __init__(self):
        self.logger = logging.getLogger('Tools')
        self.rootDir = Path(__file__).parent.parent
        self.lockFile = os.path.join(self.rootDir, '.lock')
        self.scriptPath = os.path.join(self.rootDir, 'scripts/')

    def getLockFilestatus(self):
        """ is there a Lock File? get the Lock Id """
        if (os.path.exists(self.lockFile) is False):
            return -1
        else:
            with open(self.lockFile, 'r') as f:
                last_line = f.readlines()[-1]
                # convert to int
                try:
                    result = int(last_line)
                    return result
                except Exception:
                    return -1

    def loadScript(self, filename):
        """ load a PS Script """
        path = os.path.join(self.scriptPath, filename)
        if (os.path.exists(path) is False):
            self.logger.error("Script scripts/%s does not exist -abort-" % filename)
            sys.exit()
        else:
            with open(path, 'r') as f:
                lines = f.readlines()
            return lines

    def Rename(self, filename):
        cmdarray = self.loadScript(filename)
        print(cmdarray)
        """
        this.modifyScript(cmdarray)
        this.createScript(cmdarray, filename)
        Path filepath = Paths.get(TMP_Dir + filename)

        if(FileTools.Exists(filepath) == false){
            logger.error("Script not found: " + filepath)
            this.triggerCloseEvent()
        }

        //Do the JOB
        logger.info("Renaming Host to " + host.getName())
        if(this.debug == false){
            aRuntime shell = new aRuntime()
            shell.executePSScript(filepath, true)
            // Delete tmp Script with passwords
            FileTools.Delete(Paths.get(TMP_Dir + "Rename.ps1"))
        }
        logger.info("Host Renamed---------------------------------------------")
        """

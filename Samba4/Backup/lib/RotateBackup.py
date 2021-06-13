import os
import re
import fnmatch

class RotateBackup():
    ''' A Class to Rotate Backups in form *YYYY-MM-DD.tar.bzip2 '''
    def __init__(self, versions, path, debug):
        self.versions = versions
        self.path = path
        self.debug = debug

    def cleanUp(self, ):
        """ keep versions of backups in path """
        print("Cleaning in progress")
        data = []
        # search backups
        files = self.search_files(self.path, "*.tar.bzip2")
        for f in files:
            # extract dates
            p = re.compile("\d{4}-\d{1,2}-\d{1,2}")  # noqa
            erg = p.findall(f)
            if erg:
                data.append([f, erg[0]])

        # sort with key, take the date as key
        data.sort(key=lambda the_file: the_file[1])

        limit = int(self.versions) + 1
        while len(data) >= limit:
            # delete oldest backup Versions
            cmd = "rm %s" % data[0][0]
            if self.debug is False:
                os.system(cmd)
                # remove first element
                data.pop(0)

        if self.debug is False:
            print("-done-\n")

    def search_files(self, directory, pattern):
        """ search for pattern in directory recursive """
        data = []
        for dirpath, dirnames, files in os.walk(directory):  # noqa
            for f in fnmatch.filter(files, pattern):
                data.append(os.path.join(dirpath, f))
        return data

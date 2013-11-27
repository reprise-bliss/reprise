import subprocess


class RemoteError(Exception):

    pass


class Remote:

    def __init__(self, user, host, repository):
        self.user = user
        self.host = host
        self.repository = repository

    def packages(self):
        print("packages")
        rsync = ""
        status, output = subprocess.getstatusoutput(rsync)
        if status != 0:
            raise RemoteError(
                    "rsync command returned status {}".format(status))
        print(output)


    def synchronize(self):
        print("sync")
        rsync = ""
        status, output = subprocess.getstatusoutput(rsync)
        if status != 0:
            raise RemoteError(
                    "rsync command returned status {}".format(status))



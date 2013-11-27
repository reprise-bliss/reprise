import subprocess

from magnetron.repository import Repository, RepositoryError, base_path


class RemoteError(Exception):

    pass


class Remote:

    def __init__(self, user, host, remote, local):
        self.user = user
        self.host = host
        self.remote = remote
        self.created = False
        try:
            self.local = Repository(local)
        except RepositoryError:
            self.local = Repository.create(local)
            self.created = True

    def _rsync(self, verbose=True, dry_run=True):
        n = "--dry-run " if dry_run else ""
        rsync = "rsync {}-rvz -e ssh {}@{}:{}/{} {}".format(
            n, self.user, self.host, base_path, self.remote, self.local.path)
        print(rsync)
        status, output = subprocess.getstatusoutput(rsync)
        if status != 0:
            raise RemoteError(output)
        if verbose:
            print(output)

    def packages(self):
        self._rsync(verbose=True, dry_run=True)
        if self.created:
            self.local.expunge()


    def synchronize(self):
        self._rsync(verbose=False, dry_run=False)
        # sign packages



import os
import subprocess

from magnetron.repository import Repository, RepositoryError, base_path


class RemoteError(Exception):

    pass


class Remote:

    def __init__(self, user, host, remote, local):
        self.user = user
        self.host = host
        self.remote = remote
        self.local_name = local

    def _rsync(self, verbose=True, dry_run=True):
        n = "--dry-run " if dry_run else ""
        rsync = "rsync {}-rvz -e ssh {}@{}:{}/{} {}".format(
            n, self.user, self.host, os.path.abspath(base_path),
            self.remote, os.path.abspath(self.local.path))
        status, output = subprocess.getstatusoutput(rsync)
        if status != 0:
            raise RemoteError(rsync, output)
        if verbose:
            print(output)

    def packages(self):
        self.created = False
        try:
            self.local = Repository(self.local_name)
        except RepositoryError:
            self.local = Repository.create(self.local_name)
            self.created = True
        self._rsync(verbose=True, dry_run=True)
        if self.created:
            self.local.expunge()

    def synchronize(self):
        try:
            self.local = Repository(self.local_name)
        except RepositoryError:
            self.local = Repository.create(self.local_name)
        self._rsync(verbose=False, dry_run=False)
        self.local.reinitialize()

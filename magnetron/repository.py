import subprocess


def initialize():
    pass


class RepositoryError(Exception):

    pass


class Repository:

    def __init__(self, name):
        self.name = name

    @classmethod
    def create(cls, name):
        return cls(name)

    def get(self, package, distribution):
        ''' get information about a package '''
        pass

    def add(self, filename, distribution):
        ''' add a package to this repository '''
        pass

    def remove(self, package, distribution):
        ''' remove a package from the repository '''
        pass

    def expunge(self):
        ''' delete this repository '''
        pass

    def pull(self, other):
        ''' overwrite this repository '''
        pass

    def packages(self, distribution):
        ''' list packages per distribution '''
        pass

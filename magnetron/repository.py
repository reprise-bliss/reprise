import os
import re
import shutil

import magnetron.reprepro


base_path = "/srv/magnetron"
name_re = re.compile(r'[a-zA-Z][a-zA-Z0-9_]+')
default_distributions = [
    "precise",
    "quantal",
    "raring",
    "saucy",
    "trusty",
]
distributions_template = '''Origin: {origin}
Label: {label}
Suite: {suite}
Codename: {codename}
Version: 3.0
Architectures: i386 amd64 armhf source
Components: main
Description: {description}
SignWith: {sign_with}
'''

class RepositoryError(Exception):

    pass


def initialize():
    if os.path.exists(base_path):
        raise RepositoryError("already initialized")
    os.makedirs(base_path)


def check_name(name):
    if not name_re.match(name):
        raise RepositoryError("invalid name " + repr(name))
    return name


def repositories():
    return list(sorted(Repository(i) for i in os.listdir(base_path)))


class Package:

    def __init__(self, spec):
        self.spec = spec  # e.g.: raring|main|amd64: pep8 1.3.3-0ubuntu
        try:
            self.distribution = spec.split("|")[0]
            self.architecture = spec.split("|")[2]
            self.name = spec.split()[1]
            self.version = spec.split()[2]
        except IndexError:
            raise ValueError("invalid spec: " + repr(spec))

    def __repr__(self):
        return "<Package {}>".format(repr(self.spec))


class Repository:

    def __init__(self, name):
        self.name = check_name(name)
        self.path = os.path.join(base_path, self.name)
        if not os.path.exists(base_path):
            raise RepositoryError("not initialized")
        if not os.path.exists(self.path):
            raise RepositoryError("repository doesn't exist")

    @classmethod
    def create(cls, name):
        if not os.path.exists(base_path):
            raise RepositoryError("not initialized")
        if os.path.exists(os.path.join(base_path, check_name(name))):
            raise RepositoryError("repository exists")
        os.makedirs(os.path.join(base_path, name, "conf"))
        dist = os.path.join(base_path, name, "conf", "distributions")
        with open(dist, "w") as f:
            for distribution in default_distributions:
                f.write(distributions_template.format(
                    origin=name,
                    label=name,
                    suite=distribution,
                    codename=distribution,
                    description=name,
                    sign_with="FAKE_SIGNING_KEY",  # TODO
                ).strip() + "\n")
                f.write("\n")
        return cls(name)

    def get(self, package, distribution):
        ''' get information about a package '''
        if package in (i.name for i in self.packages(distribution)):
            return [i for i in self.packages(distribution)]
        raise RepositoryError("package not found")

    def add(self, filename, distribution):
        ''' add a package to this repository '''
        if not os.path.exists(filename):
            raise FileNotFoundError(
                "[Errno 2] No such file or directory: " + repr(filename))
        magnetron.reprepro.include_deb(self.path, filename, distribution)

    def remove(self, package, distribution):
        ''' remove a package from the repository '''
        magnetron.reprepro.remove(self.path, package, distribution)

    def expunge(self):
        ''' delete this repository '''
        shutil.rmtree(self.path)

    def pull(self, other):
        ''' overwrite this repository '''
        self.expunge()
        shutil.copytree(other.path, self.path)

    def packages(self, distribution):
        ''' list packages per distribution '''
        for spec in sorted(magnetron.reprepro.list_packages(
                self.path, distribution).split("\n")):
            if spec:
                yield Package(spec)

    def __repr__(self):
        return "<Repository '{}'>".format(self.name)

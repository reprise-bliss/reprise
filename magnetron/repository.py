import os
import re
import shutil
import glob

import magnetron.gpg
import magnetron.reprepro


base_path = "/srv/magnetron"
name_re = re.compile(r'[a-zA-Z][a-zA-Z0-9_]+')
distributions_template = '''Origin: {origin}
Label: {label}
Suite: dist
Codename: dist
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
    os.makedirs(os.path.join(base_path, "incoming"))
    with open(os.path.join(base_path, "public.key"), "w") as f:
        f.write(magnetron.gpg.get_default_public_key())


def check_name(name):
    if not name_re.match(name) or name in ("incoming", ):
        raise RepositoryError("invalid name " + repr(name))
    return name


def repositories():
    ls = [i for i in os.listdir(base_path)
          if os.path.isdir(os.path.join(base_path, i))]
    ls = [i for i in ls if i not in ("incoming", )]
    return list(sorted((Repository(i) for i in ls), key=lambda i: i.name))


class Package:

    def __init__(self, spec):
        self.spec = spec  # e.g.: raring|main|amd64: pep8 1.3.3-0ubuntu
        self.architecture = spec.split("|")[2].split(":")[0]
        self.name = spec.split()[1]
        self.version = spec.split()[2]

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
            f.write(distributions_template.format(
                origin=name,
                label=name,
                description=name,
                sign_with=magnetron.gpg.get_default_key_id(),
            ).strip() + "\n")
            f.write("\n")
        return cls(name)

    def get(self, package):
        ''' get information about a package '''
        if package in (i.name for i in self.packages()):
            return [i for i in self.packages() if i.name == package]
        raise RepositoryError("package not found")

    def add(self, filename):
        ''' add a package to this repository '''
        if not os.path.exists(filename):
            raise FileNotFoundError(
                "[Errno 2] No such file or directory: " + repr(filename))
        magnetron.reprepro.include_deb(self.path, filename)

    def remove(self, package):
        ''' remove a package from the repository '''
        magnetron.reprepro.remove(self.path, package)

    def expunge(self):
        ''' delete this repository '''
        shutil.rmtree(self.path)

    def pull(self, other):
        ''' overwrite this repository '''
        self.expunge()
        shutil.copytree(other.path, self.path)

    def packages(self):
        ''' list packages '''
        for spec in sorted(magnetron.reprepro.list_packages(
                self.path).split("\n")):
            if spec:
                yield Package(spec)

    def reinitialize(self):
        ''' re-add the packages in a broken repository '''
        packages = glob.glob(os.path.join(
            self.path, "**/**/**/**/**/*.deb"))
        for i in packages:
            self.add(i)

    def __repr__(self):
        return "<Repository '{}'>".format(self.name)

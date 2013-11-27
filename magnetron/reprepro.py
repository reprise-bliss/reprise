import subprocess


def _reprepro(path, command, quiet=False):
    command = "reprepro -b {} ".format(path) + command
    stderr = subprocess.DEVNULL if quiet else None
    return subprocess.check_output(
        command, shell=True, stderr=stderr).decode("utf-8")

def list_packages(path, distribution="dist"):
    return _reprepro(path, "list " + distribution, quiet=True)


def include_deb(path, filename, distribution="dist"):
    return _reprepro(path, "includedeb {} {}".format(distribution, filename))


def remove(path, package, distribution="dist"):
    return _reprepro(path, "remove {} {}".format(distribution, package))

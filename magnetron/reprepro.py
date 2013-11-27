import subprocess


def _reprepro(path, command):
    command = "reprepro -b {} ".format(path) + command
    return subprocess.check_output(
        command, shell=True).decode("utf-8")

def list_packages(path, distribution):
    return _reprepro(path, "list " + distribution)


def include_deb(path, filename, distribution):
    return _reprepro(path, "includedeb {} {}".format(distribution, filename))


def remove(path, package, distribution):
    return _reprepro(path, "remove {} {}".format(path, distribution, package))

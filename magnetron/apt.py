import shutil
import os
import subprocess
import codecs


def run(path):
    pwd = os.getcwd()
    os.chdir(path)
    s = 0
    s = s or os.system("apt-ftparchive packages . > Packages")
    s = s or os.system("apt-ftparchive release . > Release")
    s = s or os.system("rm -f Release.gpg")
    s = s or os.system("gpg -abs -o Release.gpg Release")
    os.chdir(pwd)
    if s:
        raise RuntimeError("command returned status {:d}".format(s))


def list_packages(path, attr="Version"):
    with codecs.open(os.path.join(path, "Packages"), "r", "utf-8") as f:
        f = f.read().strip().split("\n\n")
    return [(i.split("Package: ")[1].split("\n")[0],
             i.split(attr + ": ")[1].split("\n")[0]) for i in f
            if "Package: " in i and (attr + ": ") in i]


def include_deb(path, filename):
    shutil.copy(filename, path)
    run(path)


def remove(path, package):
    packages = list_packages(path, "Filename")
    for filename in [i[1] for i in packages if i[0] == package]:
        os.remove(os.path.join(path, filename))
    run(path)

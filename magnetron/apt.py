import os
import shutil


def update_repository(path):
    ''' generate the repository metadata for all packages '''
    old_cwd = os.getcwd()
    os.chdir(path)
    if any((os.system("dpkg-scanpackages . 2>/dev/null > Packages"),
            os.system("apt-ftparchive release . > Release") or
            os.system("rm -f Release.gpg") or
            os.system("gpg -abs -o Release.gpg Release"))):
        raise RuntimeError("command returned non-zero exit status")
    os.chdir(old_cwd)


def list_packages(path, attr="Version"):
    ''' return a mapping of package names to attributes in 'Packages' '''
    with open(os.path.join(path, "Packages"), errors="replace") as f:
        return [(i.split("Package: ")[1].split("\n")[0],
                 i.split(attr + ": ")[1].split("\n")[0])
                for i in f.read().strip().split("\n\n")
                if "Package: " in i and (attr + ": ") in i]


def include_deb(path, filename):
    ''' copy a package into the repository and generate its metadata '''
    shutil.copy(filename, path)
    update_repository(path)


def remove(path, name):
    ''' delete a package from a repository '''
    for fn in [i[1] for i in list_packages(path, "Filename") if i[0] == name]:
        os.remove(os.path.join(path, fn))
    update_repository(path)

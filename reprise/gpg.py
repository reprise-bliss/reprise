import subprocess


def _run(command, quiet=False):
    stderr = subprocess.DEVNULL if quiet else None
    return subprocess.check_output(
        command, shell=True, stderr=stderr).decode("utf-8")


def get_default_public_key():
    output = _run("gpg --export -a").strip()
    if output:
        return output + "\n"
    raise ValueError("could not get default gpg key")  # pragma: no cover


def get_default_key_id():
    output = _run("gpg --list-keys").split("\n")
    for i in output:
        if i.startswith("pub ") and "/" in i and " " in i:
            return i.split("pub")[1].split("/")[1].split()[0]
    raise ValueError("could not get default gpg key id")  # pragma: no cover

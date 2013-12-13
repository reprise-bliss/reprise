'''
magnetron

Usage:
    magnetron init [<repository>]
    magnetron show [<repository> [<package>]]
    magnetron pull [-s] [<user>@]<host> <remote-repository> <repository>
    magnetron source <repository>
    magnetron include <repository> <filename>
    magnetron delete <repository> [<package>]
    magnetron update <source-repository> <repository>

Options:
    --dry-run -s  simulate pull without copying anything
    --help -h     show this screen and exit
    --version     show version number and exit

'''

import sys
import os
import pwd
import socket
import docopt

from magnetron.remote import Remote, RemoteError
from magnetron.repository import Repository, RepositoryError
from magnetron.repository import initialize, repositories, base_path
from magnetron import __version__


def init(repository=None):
    try:
        if repository is None:
            initialize()
        else:
            Repository.create(repository)
    except PermissionError as e:  # pragma: no cover
        print(e, file=sys.stderr)
        sys.exit(1)
    except RepositoryError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def show(repository=None, package=None):
    if repository is None and package is None:
        for repository in repositories():
            print(repository.name)
    elif package is None:
        try:
            seen = set()
            for i in Repository(repository).packages():
                if i.name not in seen:
                    print(i.name, i.version)
                    seen |= {i.name}
        except RepositoryError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    else:
        try:
            packages = Repository(repository).get(package)
            print(packages[0].name, packages[0].version)
        except RepositoryError as e:
            print(e, file=sys.stderr)
            sys.exit(1)


def source(repository):
    try:
        print("deb ssh://{user}@{host}:{path} /".format(
            user=pwd.getpwuid(os.getuid()).pw_name,
            host=socket.getfqdn(),
            path=os.path.abspath(Repository(repository).path),
        ))
    except RepositoryError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def include(repository, filename):
    try:
        if os.path.isabs(filename):
            package = filename
        else:
            package = os.path.join(base_path, "incoming", filename)
            if not os.path.exists(package) and os.path.exists(filename):
                package = filename
        Repository(repository).add(package)
    except RepositoryError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def delete(repository, package=None):
    try:
        if package is None:
            Repository(repository).expunge()
        else:
            Repository(repository).remove(package)
    except RepositoryError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def update(source_repository, target_repository):
    try:
        source = Repository(source_repository)
        target = Repository(target_repository)
        target.pull(source)
    except RepositoryError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def pull(host, remote_repository, local_repository, user=None, dry_run=False):
    user = user or pwd.getpwuid(os.getuid()).pw_name
    host = host.split("@")[-1]
    remote = Remote(user, host, remote_repository, local_repository)
    try:
        if dry_run:
            remote.packages()
        else:
            remote.synchronize()
    except RemoteError as e:  # pragma: no cover
        print(e, file=sys.stderr)
        sys.exit(1)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv, version=__version__)
    if args["init"]:
        init(args["<repository>"])
    elif args["show"]:
        show(args["<repository>"], args["<package>"])
    elif args["include"]:
        include(args["<repository>"], args["<filename>"])
    elif args["delete"]:
        delete(args["<repository>"], args["<package>"])
    elif args["update"]:
        update(args["<source-repository>"], args["<repository>"])
    elif args["source"]:
        source(args["<repository>"])
    elif args["pull"]:
        pull(args["<host>"], args["<remote-repository>"],
             args["<repository>"], args["<user>@"],
             args["--dry-run"])
    else:  # pragma: no cover
        raise ValueError("invalid arguments")


if __name__ == "__main__":
    main()  # pragma: no cover

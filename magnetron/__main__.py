'''
magnetron

Usage:
    magnetron init [<repository>]
    magnetron show [<repository> [<package>]]
    magnetron pull [--dry-run] [<user>@]<host> <remote-repository>\
 <local-repository>
    magnetron upload <repository> <file>
    magnetron delete <repository> [<package>]
    magnetron update <source-repository> <target-repository>

Options:
    --help -h   show this screen and exit

'''

import sys, os
import docopt

from magnetron.remote import Remote, RemoteError
from magnetron.repository import Repository, RepositoryError
from magnetron.repository import initialize, repositories


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
            for i in Repository(repository).packages():
                print(i)
        except RepositoryError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    else:
        try:
            for i in Repository(repository).get(package):
                print(i)
        except RepositoryError as e:
            print(e, file=sys.stderr)
            sys.exit(1)


def upload(repository, filename):
    try:
        Repository(repository).add(filename)
    except RepositoryError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
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
    user = user or os.getlogin()
    host = host.split("@")[-1]
    remote = Remote(user, host, remote_repository, local_repository)
    try:
        if dry_run:
            remote.packages()
        else:
            remote.synchronize()
    except RemoteError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    if args["init"]:
        init(args["<repository>"])
    elif args["show"]:
        show(args["<repository>"], args["<package>"])
    elif args["upload"]:
        upload(args["<repository>"], args["<file>"])
    elif args["delete"]:
       delete(args["<repository>"], args["<package>"])
    elif args["update"]:
       update(args["<source-repository>"], args["<target-repository>"])
    elif args["pull"]:
       pull(args["<host>"], args["<remote-repository>"],
            args["<local-repository>"], args["<user>@"],
            bool(args["--dry-run"]))
    else:  # pragma: no cover
        raise ValueError("invalid arguments")


if __name__ == "__main__":
    main()  # pragma: no cover

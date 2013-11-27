'''
magnetron

Usage:
    magnetron init [<repository>]
    magnetron show [<repository> <distribution> [<package>]]
    magnetron pull [--dry-run] [<user>@]<host> <repository>
    magnetron upload <repository> <distribution> <file>
    magnetron delete <repository> [<distribution> <package>]
    magnetron update <source-repository> <target-repository>

Options:
    --help -h   show this screen and exit

'''

import sys, os
import docopt

from magnetron.remote import Remote, RemoteError
from magnetron.repository import Repository, RepositoryError, initialize


def init(repository=None):
    try:
        if repository is None:
            initialize()
        else:
            Repository.create(repository)
    except PermissionError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except RepositoryError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def show(repository=None, distribution=None, package=None):
    if repository is None and distribution is None and package is None:
        try:
            print("guru meditation")
        except RepositoryError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    elif package is None and distribution is not None:
        for i in Repository(repository).packages(distribution):
            print(i)
    elif package is not None:
        print(Repository(repository).get(package, distribution))
    else:
        docopt.docopt(__doc__, argv=[])  # raises SystemExit


def upload(repository, distribution, filename):
    try:
        Repository(repository).add(filename, distribution)
    except RepositoryError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def delete(repository, distribution=None, package=None):
    try:
        if package is None:
            Repository(repository).expunge()
        else:
            Repository(repository).remove(package, distribution)
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


def pull(host, repository, user=None, dry_run=False):
    user = user or os.getlogin()
    remote = Remote(user, host, repository)
    try:
        if dry_run:
            remote.packages()
        else:
            remote.synchronize()
            # sign all repos
    except RemoteError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    if args["init"]:
        init(args["<repository>"])
    elif args["show"]:
        show(args["<repository>"], args["<distribution>"], args["<package>"])
    elif args["upload"]:
        upload(args["<repository>"], args["<distribution>"], args["<file>"])
    elif args["delete"]:
       delete(args["<repository>"], args["<distribution>"], args["<package>"])
    elif args["update"]:
       update(args["<source-repository>"], args["<target-repository>"])
    elif args["pull"]:
       pull(args["<host>"], args["<repository>"], args["<user>@"],
            bool(args["--dry-run"]))
    else:
        raise ValueError("invalid arguments")


if __name__ == "__main__":
    main()

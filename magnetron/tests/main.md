# Magnetron Command Line API

This document provides examples on how to use the magnetron command-line api.

    >>> shutil.rmtree(base_path, ignore_errors=True)

Command: `magnetron init`

    >>> main("init")
    >>> main("init")
    already initialized

Command: `magnetron init <repository>`

    >>> main("init", "test-repo")

Command: `magnetron source <repository>`

    >>> main("source", "test-repo")
    deb ssh://...@localhost:/home/vagrant/magnetron/.tests_srv/test-repo dist main

    >>> main("source", "does-not-exist")
    repository doesn't exist

Command: `magnetron show`

    >>> main("show")
    test-repo

Command: `magnetron show <repository>`

    >>> main("show", "test-repo")
    >>> main("show", "hello-repo")
    repository doesn't exist

Command: `magnetron show <repository> <package>`

    >>> main("show", "test-repo", "hello")
    package not found

Command: `magnetron upload <repository> <file>`

    >>> filename = glob.glob("/var/cache/apt/archives/pep8_*_all.deb")[0]
    >>> main("upload", "test-repo", filename)

    >>> main("upload", "test-repo", filename + ".broken")
    [Errno 2] No such file or directory: ...

    >>> main("upload", "doesn't exist", filename)
    repository doesn't exist

    >>> main("show", "test-repo", "pep8")
    pep8 ...-0ubuntu1 (amd64, armhf, i386)

Command: `magnetron update <source-repository> <target-repository>`

    >>> main("init", "test-repo-2")
    >>> main("update", "test-repo", "test-repo-2")
    >>> main("show", "test-repo")
    pep8 ...-0ubuntu1
    >>> main("update", "doesn't exist", "test-repo-2")
    repository doesn't exist

Command: `magnetron delete <repository> <package>`

    >>> main("delete", "test-repo", "pep8")
    >>> main("show", "test-repo")

Command: `magnetron delete <repository>`

    >>> main("show")
    test-repo
    test-repo-2

    >>> main("delete", "test-repo")
    >>> main("show")
    test-repo-2
    >>> main("delete", "test-repo-2")
    >>> main("show")

    >>> main("delete", "doesnt-exist")
    repository doesn't exist

Command: `magnetron pull`

    >>> main("init", "remote")
    >>> main("upload", "remote", filename)

    >>> main("pull", "--dry-run", "localhost", "remote", "local")
    receiving incremental file list
    remote/
    ...
    remote/pool/
    ...
    total size is ...  speedup is ... (DRY RUN)

    >>> main("pull", "localhost", "remote", "local")
    >>> main("show", "local")
    pep8 1.3.3-0ubuntu1

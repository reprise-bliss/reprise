# Reprise Command Line API

This document provides examples on how to use the reprise command-line api.

    >>> shutil.rmtree(base_path, ignore_errors=True)

Command: `reprise init`

    >>> main("init")
    >>> main("init")
    already initialized

Command: `reprise init <repository>`

    >>> main("init", "test-repo")

Command: `reprise source <repository>`

    >>> main("source", "test-repo")
    deb ssh://...@...:/home/vagrant/reprise/.tests_srv/test-repo dist main

    >>> main("source", "does-not-exist")
    repository doesn't exist

Command: `reprise show`

    >>> main("show")
    test-repo

Command: `reprise show <repository>`

    >>> main("show", "test-repo")
    >>> main("show", "hello-repo")
    repository doesn't exist

Command: `reprise show <repository> <package>`

    >>> main("show", "test-repo", "hello")
    package not found

Command: `reprise include <repository> <filename>`

    >>> filename = glob.glob("/var/cache/apt/archives/pep8_*_all.deb")[0]
    >>> _ = shutil.copy(filename, os.path.join(base_path, "incoming"))
    >>> main("include", "test-repo", os.path.basename(filename))

    >>> main("include", "test-repo", filename + ".broken")
    [Errno 2] No such file or directory: ...

    >>> main("include", "doesn't exist", filename)
    repository doesn't exist

    >>> main("show", "test-repo", "pep8")
    pep8 ... (amd64, armhf, i386)

Command: `reprise update <source-repository> <target-repository>`

    >>> main("init", "test-repo-2")
    >>> main("update", "test-repo", "test-repo-2")
    >>> main("show", "test-repo")
    pep8 ...
    >>> main("update", "doesn't exist", "test-repo-2")
    repository doesn't exist

Command: `reprise delete <repository> <package>`

    >>> main("delete", "test-repo", "pep8")
    >>> main("show", "test-repo")

Command: `reprise delete <repository>`

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

Command: `reprise pull`

    >>> main("init", "remote")
    >>> main("include", "remote", filename)

    >>> main("pull", "--dry-run", "localhost", "remote", "local")
    receiving incremental file list
    remote/
    ...
    remote/pool/
    ...
    total size is ...  speedup is ... (DRY RUN)

    >>> main("pull", "localhost", "remote", "local")
    >>> main("show", "local")
    pep8 ...

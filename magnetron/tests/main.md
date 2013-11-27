# Magnetron Command Line API

This document provides examples on how to use the magnetron command-line api.

    >>> shutil.rmtree(base_path, ignore_errors=True)

Command: `magnetron init`

    >>> main("init")
    >>> main("init")
    already initialized

Command: `magnetron init <repository>`

    >>> main("init", "test-repo")

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
    <Package ... pep8...
    ...

Command: `magnetron update <source-repository> <target-repository>`

    >>> main("init", "test-repo-2")
    >>> main("update", "test-repo", "test-repo-2")
    >>> main("show", "test-repo")
    <Package ... pep8...
    ...
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

# Magnetron Main Integration Test

This test will go over all of the available features of the command line API
and run them on the local host. To prepare for this, the user executing this
test must have write access to the `/srv/` directory.

The API of the repository class (`magnetron.repository.Repository`) is quite
similar to the command line api implemented in (`magnetron.__main__`), which
is tested separately.

## Initializing the host

Magnetron stores all of the data in `/srv/magnetron`, which we will remove
first of all:

    >>> shutil.rmtree("/srv/magnetron", ignore_errors=True)

We can now use `magnetron init` to initialize the files needed on the server:

    >>> initialize()
    >>> os.listdir(base_path)
    []

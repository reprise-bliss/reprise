import doctest
import io
import pkg_resources


def load_tests(loader, tests, ignore):
    import shutil
    import os.path
    import glob
    import reprise.repository
    reprise.repository.base_path = "./.tests_srv"
    shutil.rmtree(reprise.repository.base_path, ignore_errors=True)
    from reprise.repository import Repository, RepositoryError
    from reprise.repository import initialize, repositories, base_path
    from reprise.remote import Remote
    from reprise.gpg import get_default_public_key, get_default_key_id
    from reprise.__main__ import main as _main

    def main(*a):
        try:
            import sys
            stdout, stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
            _main(list(a))
        except SystemExit:
            pass
        finally:
            sys.stdout.seek(0)
            sys.stderr.seek(0)
            result = (sys.stdout.read().strip() + "\n" +
                      sys.stderr.read().strip())
            sys.stdout, sys.stderr = stdout, stderr
        print(result.strip())

    globs = {}
    globs.update({k: v for k, v in globals().items()})
    globs.update({k: v for k, v in locals().items()})
    for fn in ["integration.md", "main.md"]:
        fn = os.path.relpath(os.path.join(
            os.path.dirname(__file__), "..", "tests", fn))
        tests.addTests(doctest.DocFileSuite(
            fn, globs=globs,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE))
    return tests


__version__ = pkg_resources.get_distribution("reprise").version

import io
import doctest


def load_tests(loader, tests, ignore):
    import shutil
    import os.path
    import glob
    import magnetron.repository
    magnetron.repository.base_path = "./.tests_srv"
    shutil.rmtree(magnetron.repository.base_path, ignore_errors=True)
    from magnetron.repository import Repository, RepositoryError
    from magnetron.repository import initialize, repositories, base_path
    from magnetron.remote import Remote
    from magnetron.gpg import get_default_public_key, get_default_key_id
    from magnetron.__main__ import main as _main

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

import os.path
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
    globs = {}
    globs.update({k: v for k, v in globals().items()})
    globs.update({k: v for k, v in locals().items()})
    for fn  in ["integration.md"]:
        fn = os.path.relpath(os.path.join(
            os.path.dirname(__file__), "..", "tests", fn))
        tests.addTests(doctest.DocFileSuite(
            fn, globs=globs, optionflags=doctest.ELLIPSIS))
    return tests

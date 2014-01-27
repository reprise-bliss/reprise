from setuptools import setup

setup(
    name="reprise",
    version="0.1.0",
    packages=[
        "reprise",
    ],
    test_suite="reprise",
    install_requires={
        "docopt",
    },
    entry_points={
        "console_scripts": [
            "reprise = reprise.__main__:main",
        ],
    },
    data_files=[
        ("share/man/man1", ["debian/reprise.1"]),
    ],
)

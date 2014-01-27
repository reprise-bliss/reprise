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
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: System :: Archiving :: Packaging",
    ],
)

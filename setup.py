from setuptools import setup

setup(
    name="magnetron",
    version="0.1.0",
    packages=[
        "magnetron",
    ],
    test_suite="magnetron",
    install_requires={
        "docopt",
    },
    entry_points={
        "console_scripts": [
            "magnetron = magnetron.__main__:main",
        ],
    },
    data_files=[
        ("share/man/man1", ["debian/magnetron.1"]),
    ],
)

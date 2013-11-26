from setuptools import setup

setup(
    name="magnetron",
    packages=[
        "magnetron",
    ],
    install_requires={
        "docopt",
    },
    entry_points={
        "console_scripts": [
            "magnetron = magnetron.__main__:main",
        ],
    },
)

import setuptools

with open("asent/about.py") as f:
    v = f.read()
    for line in v.split("\n"):
        if line.startswith("__version__"):
            __version__ = line.split('"')[-2]


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(version=__version__)

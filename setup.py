import setuptools

with open("asent/about.py") as f:
    v = f.read()
    for l in v.split("\n"):
        if l.startswith("__version__"):
            __version__ = l.split('"')[-2]


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(version=__version__)

import setuptools


with open("asent/about.py") as f:
    v = f.read()
    for l in v.split("\n"):
        if l.startswith("__version__"):
            __version__ = l.split('"')[-2]


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="asent",
    version=__version__,
    description="A python package for flexible and transparent sentiment analysis.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="K. Enevoldsen",
    url="https://github.com/KennethEnevoldsen/asent",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data = {"sentida":['emoji_utf8_lexicon.txt', 'sentidav2_lemmas.csv'],},
    # external packages as dependencies
    install_requires=["spacy>=3.0.0,<3.2.0"],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="NLP danish",
)

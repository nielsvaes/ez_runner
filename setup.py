from pkg_resources import DistributionNotFound, get_distribution
import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

data_files_to_include = ["*.png"]
requires = []


def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None


if sys.version_info.major >= 3 and sys.version_info.minor >= 7:
    if get_dist("pyside6") is None and get_dist("pyside2") is None:
        requires.append("pyside6")
else:
    if get_dist("pyside2") is None:
        requires.append("pyside2")

setuptools.setup(
    name="ez-runner",
    version="1.0.0",
    author="Niels Vaes",
    license='MIT',
    author_email="nielsvaes@gmail.com",
    description="Qt Runner framework for easy threading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nielsvaes/ez_runner",
    install_requires=requires,
    packages=setuptools.find_packages(),
    package_data={
        "": data_files_to_include,
    },
    classifiers=[
        "Operating System :: OS Independent",
    ]
)

import os
from setuptools import setup, find_packages
import trackman


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


setup(
    name="django-trackman",
    version=trackman.__version__,
    description=read("DESCRIPTION"),
    long_description=read("README.rst"),
    keywords="trackman django log logging tracking activity",
    packages=find_packages(),
    author="",
    author_email="",
    url="https://github.com/lazybird/django-trackman/",
    include_package_data=True,
)

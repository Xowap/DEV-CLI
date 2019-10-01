# coding: utf-8
from __future__ import unicode_literals

import codecs
import os

from setuptools import find_packages, setup

try:
    from pip.req import parse_requirements
    from pip.download import PipSession
except ImportError:
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession

rf = codecs.open(os.path.join(os.path.dirname(__file__), "README.txt"), "r")
with rf as readme:
    README = readme.read()

with PipSession() as s:
    requirements = parse_requirements(
        os.path.join(os.path.dirname(__file__), "requirements_as_lib.txt"), session=s
    )

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="dev-cli",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    license="WTFPL",
    description="A CLI interface for dev.to",
    long_description=README,
    url="https://github.com/Xowap/DEV-CLI",
    install_requires=[str(x.req) for x in requirements],
    author="Rémy Sanchez",
    author_email="remy.sanchez@hyperthese.net",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)

import os
from glob import glob
from os.path import basename, splitext

import setuptools

base_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_path, "README.md")) as f:
    README = f.read()

REQUIREMENTS = ["influxdb-client", "python-dotenv", "requests"]

setuptools.setup(
    name="intervalsicu_to_influxdb",
    version="0.1.0",
    description="A package to extract data from intervals.icu to influxDB",
    url="https://codeberg.org/tmllull/intervalsicu-to-influxdb",
    author="Toni Miquel Llull",
    author_email="tonimiquel.llull@gmail.com",
    license="GPL3",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    # packages=setuptools.find_packages(exclude=("tests*",)),
    python_requires=">=3",
    keywords=["intervalsicu", "influxdb", "sport"],
    install_requires=REQUIREMENTS,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
)

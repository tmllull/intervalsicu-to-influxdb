import os
from glob import glob
from os.path import basename, splitext

import setuptools

try:
    if os.environ.get("CI_COMMIT_TAG"):
        version = os.environ["CI_COMMIT_TAG"]
    else:
        version = os.environ["CI_JOB_ID"]
except KeyError:
    version = "0.2.41"

REQUIREMENTS = ["influxdb-client", "python-dotenv", "requests"]

setuptools.setup(
    version=version,
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    install_requires=REQUIREMENTS,
)

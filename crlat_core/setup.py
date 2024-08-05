from setuptools import setup, find_packages
import os
base_version = '0.2'
try:
    with open(os.path.join(os.path.split(__file__)[0], 'version.txt')) as f:
        build_no = f.read().strip()
except FileNotFoundError as e:
    print('WARNING! exception "%s" is ok for local development but critical on CI' % e)
    build_no = 0

version = '%s.%s' % (base_version, build_no)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="crlat_core",
    version=version,
    author="Coral Automation",
    author_email="",
    description="A core package for crlat project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[
        'requests==2.28.2',
        # -*- Extra requirements: -*-
    ],
)

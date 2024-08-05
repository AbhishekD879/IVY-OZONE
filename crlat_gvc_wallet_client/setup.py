import os

from setuptools import find_packages
from setuptools import setup

base_version = '0.3'
try:
    with open(os.path.join(os.path.split(__file__)[0], 'version.txt')) as f:
        build_no = f.read().strip()
except FileNotFoundError as e:
    print(f'WARNING! exception "{e}" is ok for local development but critical on CI')
    build_no = 0


version = f'{base_version}.{build_no}'


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='crlat-gvc-wallet-client',
      version=version,
      description='GVC User client',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='GVC Automation',
      author_email='',
      url='https://bitbucket.org/symphonydevelopers/crlat_gvc_wallet_client',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,  # Specifying the files to distribute: https://docs.python.org/3/distutils/sourcedist.html#the-manifest-in-template
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'crlat-core>=0.1.30',
          'pyyaml',
          'Faker',
          'lxml'
      ],
      entry_points="""
       # -*- Entry points: -*-
       """,
      )

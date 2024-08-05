import os

from setuptools import find_packages
from setuptools import setup

base_version = '1.5'
try:
    with open(os.path.join(os.path.split(__file__)[0], 'version.txt')) as f:
        build_no = f.read().strip()
except FileNotFoundError as e:
    print('WARNING! exception "%s" is ok for local development but critical on CI' % e)
    build_no = 0

version = '%s.%s' % (base_version, build_no)

setup(name='crlat_behave_core',
      version=version,
      description='Backend integration frameworks Behave core utils',
      long_description="""\
      """,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      # Specifying the files to distribute: https://docs.python.org/3/distutils/sourcedist.html#the-manifest-in-template
      zip_safe=False,
      install_requires=[
          'behave',
          'ujson==1.35',
          'requests==2.19.1',
          'certifi>=14.05.14',
          'six>=1.10',
          'setuptools>=21.0.0',
          'urllib3<1.24,>=1.21.1',
          'jsonpath-ng',
          'pymongo',
          'environs',
          'pyyaml==5.1',
          'crlat_ob_client>=0.8.225',
          'crlat-testrail-integration-client>=2.0.16',
          'crlat-swagger-client>=1.0.7'
      ],
      entry_points="""
       # -*- Entry points: -*-
       """,
      )

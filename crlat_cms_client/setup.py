import os

from setuptools import find_packages
from setuptools import setup

base_version = '4.2'
try:
    with open(os.path.join(os.path.split(__file__)[0], 'version.txt')) as f:
        build_no = f.read().strip()
except FileNotFoundError as e:
    print('WARNING! exception "%s" is ok for local development but critical on CI' % e)
    build_no = 0


version = '%s.%s' % (base_version, build_no)

setup(name='crlat-cms-client',
      version=version,
      description="CMS API client",
      long_description="""\
      """,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,  # Specifying the files to distribute: https://docs.python.org/3/distutils/sourcedist.html#the-manifest-in-template
      zip_safe=False,
      install_requires=[
          'crlat-core>=0.1.30',
          'requests==2.28.2',
          'Faker',
          'lxml',
          'tenacity==8.2.2',
          'pyyaml',
          'pytz'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
       # -*- Entry points: -*-
       """,
      )

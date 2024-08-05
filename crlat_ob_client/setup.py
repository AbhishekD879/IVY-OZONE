import os

from setuptools import find_packages
from setuptools import setup


with open(os.path.join(os.path.split(__file__)[0], 'version.txt')) as f:
    lines = f.readlines()

version = '0.9.%s' % next(line.rstrip('\n') for line in lines)

setup(name='crlat-ob-client',
      version=version,
      description="Open Bet client",
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
          'requests==2.28.2',
          'psutil==5.9.5',
          'Faker',
          'lxml',
          'six>=1.5',
          'crlat-siteserve-client>=0.6.33',
          'pyyaml',
          'pytz',
          'tenacity==8.2.2',
          'crlat-core>=0.1.30'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
       # -*- Entry points: -*-
       """,
      )

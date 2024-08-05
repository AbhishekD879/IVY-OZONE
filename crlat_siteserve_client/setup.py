import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.split(__file__)[0], 'version.txt')) as f:
    lines = f.readlines()

version = '0.7.%s' % next(line.rstrip('\n') for line in lines)

setup(name='crlat-siteserve-client',
      version=version,
      description="",
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
      zip_safe=False,
      install_requires=[
          'requests==2.28.2',
          'psutil==5.9.5',
          'lxml',
          'six>=1.5',
          'pytz',
          'pyyaml'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
       # -*- Entry points: -*-
       """,
      )


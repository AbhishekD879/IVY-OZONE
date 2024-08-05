import os

from setuptools import find_packages
from setuptools import setup

base_version = '1.0'
try:
    with open(os.path.join(os.path.split(__file__)[0], 'version.txt')) as f:
        build_no = f.read().strip()
except FileNotFoundError as e:
    print('WARNING! exception "%s" is ok for local development but critical on CI' % e)
    build_no = 0


version = '%s.%s' % (base_version, build_no)

setup(name='crlat-swagger-client',
      version=version,
      description="Oxygen CMS REST API",
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
      install_requires=["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"],
      entry_points="""
       # -*- Entry points: -*-
       """,
      )

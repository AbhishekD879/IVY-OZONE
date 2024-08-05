import os

from setuptools import find_packages
from setuptools import setup

try:
    with open(os.path.join(os.path.split(__file__)[0], 'version.txt')) as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = '1'

version = '2.2.%s' % next(line.rstrip('\n') for line in lines)

setup(
    name='crlat-testrail-integration-client',
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
        'lxml',
        'secretstorage==3.3.3',
        'keyring==23.13.1',
        'influxdb',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
        [console_scripts]
        close_old_runs = crlat_testrail_integration.scripts.close_old_runs:main
        create_data_for_email = crlat_testrail_integration.scripts.create_data_for_email:main
        create_results_file = crlat_testrail_integration.scripts.create_results_file:main
        create_run = crlat_testrail_integration.scripts.create_run:main
        remove_untested_tests = crlat_testrail_integration.scripts.remove_untested_tests:main
        # -*- Entry points: -*-
    """,
)

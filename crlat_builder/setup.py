from setuptools import setup, find_packages
version = '0.0'

setup(
    name='crlat_builder',
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
        'docker',
        'gitpython',
        'jinja2'
        # -*- Extra requirements: -*-
    ],
    entry_points="""

    [console_scripts]
      crlat_builder = crlat_builder.image_builder:main
      # -*- Entry points: -*-
      """,
)

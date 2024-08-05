from setuptools import setup, find_packages


version = '0.1'

setup(name='crlat-yourcall',
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
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'env']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'crlat-ob-client',
          'web.py',
          'cryptography',
          'pyopenssl'

          # -*- Extra requirements: -*-
      ],
      dependency_links=['https://pypi_user:secret1@pypi.crlat.net/simple/crlat-ob-client',
                        'https://pypi_user:secret1@pypi.crlat.net/simple/crlat-siteserve-client',
                        'https://pypi_user:secret1@pypi.crlat.net/simple/crlat-testrail-integration',
                        'https://pypi_user:secret1@pypi.crlat.net/simple/openapi-client'],
      entry_points="""
       # -*- Entry points: -*-
       """,
      )

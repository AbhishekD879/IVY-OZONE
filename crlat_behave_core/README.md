# crlat_behave_core



### The repository contains the main utils and functionality: 

  * Data clean up (teardown CMS modules);
  * Mongo DB client for communication with CMS Mongo;
  * OB client for creating events data and use it in Wire MockServer purpose;
  * TestRail reporter for sending test report to TestRail;
  * Utils for parsing, verifying data and datatime setup

which will be using by all Backend integration Frameworks:  

  * CMS (https://bitbucket.org/symphonydevelopers/back-end-integration-tests/src/master/);
  * Sports Featured (https://bitbucket.org/symphonydevelopers/sports_featured_backend_integration_tests/src/master/); 
  * InPlay (https://bitbucket.org/symphonydevelopers/inplay_backend_integration_tests/src/master/);


##### To build and install using pip:
- to build:
  ```
  $ python setup.py sdist
  ```
- to install package, simply use pip:
  ```
  $ pip install crlat_behave_core
  ```
- to install from tar file:
  ```
  $ pip install <path_to_distribution/filename.tar.gz>
  ```

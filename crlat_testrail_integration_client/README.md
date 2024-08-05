##### To check testrail api is enabled for user

run in terminal:
```shell
curl -H "Content-Type: application/json" -u "YOUR@EMAIL.COM:YOUR_PASSWORD" "https://ladbrokescoral.testrail.com/index.php?/api/v2/get_case/1"
```
where `YOUR@EMAIL.COM` – is your actual testrail email and `YOUR_PASSWORD` - your password

if result is a dict with test case data or `{"error":"Field :case_id is not a valid test case."}` – it means that Authentication works correctly

In case of `{"error":"Authentication failed: invalid or missing user\/password or session cookie."}`: try to [generate Testrail API key](https://docs.gurock.com/testrail-api2/accessing#username_and_api_keyhttp:// "generate Testrail API key") and use it instead of password for the `curl` command above

------------

##### To use project:
1) install using pip install
``` shell
$ pip install crlat-testrail-integration-client
```

2) set keyring pass. (it's better to set it before usage)
``` shell
python -c "import keyring; keyring.set_password('testrail_username', 'username', 'YOUR_TESTRAIL_MAIL'); keyring.set_password('testrail_password', 'password', 'YOUR_TESTRAIL_PASS')"
```
WARN: instead of `YOUR_TESTRAIL_MAIL` and `YOUR_TESTRAIL_PASS` please set your testrail email and password/api token

NOTE: in case of getting `keyring.errors.PasswordSetError: Can't store password on keychain.` try:

 1)
 ``` shell
 codesign -f -s - /path/to/virtualenv/bin/python
 ```
  [source](https://github.com/jaraco/keyring/issues/219#issuecomment-280507822 "source")

 2) on your Mac OS X open Keychain Access, find keychain Login, lock and unlock it and retry to set keyring password


------------

##### To build and install using pip:
- to build:
``` shell
$ python setup.py sdist
```
- to install package, simply use pip:
```shell
$ pip install crlat-testrail-integration-client
```
- to install from tar file:
``` shell
$ pip install <path_to_distribution/filename.tar.gz>
```
import os
import subprocess
import argparse
import sys
import threading
import signal  # Import the signal module for handling signals
from concurrent.futures import ThreadPoolExecutor, as_completed
from voltron.environments.devices import Devices
from voltron.environments.hosts import hosts

# this script can be used to run the test suite local by changing markers and custom markers same as you provide in jenkins
#  you can also run this through cmd by command python test_execution_locally.py and the arguments such
#  as mark and custom marker

# firsts it will run the jenkins_test_discovery in the project and create the mobile.txt and desktop.txt
# you can delete it once execution is completed don't push the mobile.txt and desktop.txt to main branch

# Initialize argument parser
parser = argparse.ArgumentParser()

# Define command line arguments

# Hostname argument: used as a base for URLs
parser.add_argument('--hostname', action='store', default=hosts.LADBROKES_PROD,
                    help='Provide hostname as a base for URLs, e.g., --hostname=invictus.coral.co.uk')

# Device name argument: specifies the device for testing, e.g., Galaxy S9, Desktop Chrome, etc.
parser.add_argument('--device_name', action='store', default=Devices.GALAXY_S9,
                    help='Select device name: Galaxy S9, Note 4, Nexus 5, iPhone 6S, S7, S8, Desktop Chrome, etc.')

# Device type argument: specifies whether the device is mobile or desktop
parser.add_argument('--device_type', action='store', default='Desktop',
                    help='Select device type: mobile or Desktop.')

# Test path argument: specifies the path where test cases are located
parser.add_argument('--test_path', action='store',
                    default='tests_sanity',
                    help='Specify the path where test cases are located.')

# Custom mark argument: specifies a custom mark for the tests
parser.add_argument('--custom_mark', default='sanity and not slow and not lotto', type=str,
                    help='Specify a custom mark for the tests.')

# Mark argument: specifies a mark for the tests (default is 'prod')
parser.add_argument('--mark', default='prod or lad_prod', type=str,
                    help='Specify a mark for the tests. Default is "prod".')

# Parse the command line arguments
args = parser.parse_args()

# Global flag to track interrupt signal
interrupt_flag = threading.Event()


# Function to handle interrupt signal
def signal_handler(sig, frame):
    print("\nExecution interrupted. Stopping all tests...")
    interrupt_flag.set()


# Register signal handler for interrupt signal (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Relative path to the virtual environment activate script
venv_activate_script = './venv'

# Set up environment variables based on command line arguments
env = os.environ.copy()
env['MARK'] = args.mark
env['CUSTOM_MARKS'] = args.custom_mark
env['TEST_PATH'] = args.test_path
env['RUN_ON'] = args.device_type.lower()
env['OX_HOSTNAME'] = args.hostname
# provide the test rail id here to update the results
env['TESTRAIL_ID'] = ""
if env['TESTRAIL_ID']:
    env['LOCATION_NAME'] = 'GRID_IDE'
    """use this command to set the username password if it throws test rail username password error 
    python - c "import keyring; keyring.set_password('testrail_username', 'username', 'YOUR_TESTRAIL_MAIL'); keyring.set_password('testrail_password', 'password', 'YOUR_TESTRAIL_PASS')"
    """

# Run the second script with the provided environment variables
subprocess.run(['python', 'jenkins_test_discovery.py'], env=env)


# Function to run pytest for each test path
def run_pytest(test_path, failed_tests):
    if not interrupt_flag.is_set():  # Check if interrupt signal is received
        env['test_name'] = test_path
        command = f'py.test {test_path} --hostname={args.hostname} --environment=tst2 --device_name="{args.device_name}"'
        result = subprocess.run(command, shell=True, env=env)
        exit_code = result.returncode
        if exit_code != 0:
            failed_tests.append(test_path)
            print(f"\033[91mTest {test_path} failed with exit code {exit_code}\033[0m")  # Print failed tests in red


# Determine the file name based on the device type provided
if args.device_type.title() == "Desktop":
    file_name = 'discovered-tests/desktop.txt'
elif args.device_type.title() == "Mobile":
    file_name = 'discovered-tests/mobile.txt'
else:
    raise Exception("Invalid device type. Please provide 'mobile' or 'desktop'.")

# Check if the virtual environment activation script exists
if not os.path.exists(venv_activate_script):
    print("Virtual environment activation script not found. Please provide the correct path.")
    sys.exit(1)

# Read the test paths from the text file
with open(file_name, 'r') as file:
    test_paths = file.readlines()

# Activate the virtual environment
activate_command = f'call "{venv_activate_script}"'
subprocess.run(activate_command, shell=True)

# Strip newline characters from the test paths
test_paths = [path.strip() for path in test_paths]

# Use ThreadPoolExecutor to run subprocesses in parallel
failed_tests = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(run_pytest, test_path, failed_tests) for test_path in test_paths]
    for future in as_completed(futures):
        if not interrupt_flag.is_set():  # Check if interrupt signal is received
            future.result()
        else:
            executor.shutdown(wait=False)
            sys.exit(1)

# Print the number of test cases passed and failed with color-coded formatting
print(f"\n\033[1mTests Passed: \033[92m{len(test_paths) - len(failed_tests)}\033[0m")
print(f"\033[1mTests Failed: \033[91m{len(failed_tests)}\033[0m")

# Print failed test paths in red color
print("\n\033[1mFailed Tests:\033[0m")
for test_path in failed_tests:
    print(f"\033[91m{test_path}\033[0m")  # Print failed test paths in red color

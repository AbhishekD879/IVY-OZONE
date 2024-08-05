import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from voltron.environments.browser_stack_devices import BS_Devices
from voltron.environments.hosts import hosts

venv_activate_script = r'/Users/abhishek.diwate/Desktop/Automation/lcg_uat/venv'  # Replace with your venv activate script path

if not os.path.exists(venv_activate_script):
    print("Virtual environment activation script not found. Please provide the correct path.")
    sys.exit(1)
# Read the test paths from the text file
with open('/Users/abhishek.diwate/Desktop/Automation/lcg_uat/discovered-tests/mobile.txt', 'r') as file:
    test_paths = file.readlines()

# Activate the virtual environment
activate_command = f'call "{venv_activate_script}"'
subprocess.run(activate_command, shell=True)

# Strip newline characters from the test paths
test_paths = [path.strip() for path in test_paths]

# Parameters for the py.test command
hostname = hosts.CORAL_PROD
browser_stack_device = BS_Devices.SAMSUNG_GALAXY_S9_ANDROID_V8_0_ANDROID
# Set environment variables before executing the command
env = os.environ.copy()


# Loop through each test path and run the py.test command

# for test_path in test_paths:
#     command = f"py.test /Users/abhishek.diwate/Desktop/Automation/lcg_uat/{test_path} --hostname={hostname} -v --junit-xml=results.xml --browser_stack_device={browser_stack_device} --environment=tst2 --device_name='Galaxy_S9'"
#     subprocess.run(command, shell=True, env=env)


def run_pytest(test_path):
    command = f"py.test /Users/abhishek.diwate/Desktop/Automation/lcg_uat/{test_path} --hostname={hostname} -v --junit-xml=results.xml --browser_stack_device={browser_stack_device} --environment=tst2 --device_name='iPhone_X' --use_browser_stack=True, --build_name='SANITY_PROD_MOBILE1'"
    subprocess.run(command, shell=True, env=env)
    # Add additional error handling or process output as needed


# Use ThreadPoolExecutor to run subprocesses in parallel
with ThreadPoolExecutor(max_workers=20) as executor:
    # Create a list to keep track of running futures
    running_futures = []

    # Submit the initial 6 test paths to start the execution
    for test_path in test_paths[:20]:
        future = executor.submit(run_pytest, test_path)
        running_futures.append(future)

    # Process remaining test paths
    for test_path in test_paths[20:]:
        # Wait for any of the running futures to finish before submitting a new test path
        completed_future = as_completed(running_futures)
        for future in completed_future:
            running_futures.remove(future)
            new_future = executor.submit(run_pytest, test_path)
            running_futures.append(new_future)
            break  # Break after submitting a new test path

    # Wait for the remaining tests to finish
    for future in as_completed(running_futures):
        pass  # Do nothing, just wait for completion

# The code above ensures that at most 6 tests are running concurrently at any time.

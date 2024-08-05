import os
import subprocess
import sys
from voltron.environments.browser_stack_devices import BS_Devices
from voltron.environments.hosts import hosts

venv_activate_script = r'C:\Automation\lcg_uat\venv\Scripts\activate'  # Replace with your venv activate script path

if not os.path.exists(venv_activate_script):
    print("Virtual environment activation script not found. Please provide the correct path.")
    sys.exit(1)
# Read the test paths from the text file
with open('C:\Automation\lcg_uat\discovered-tests\mobile.txt', 'r') as file:
    test_paths = file.readlines()

# Activate the virtual environment
activate_command = f'call "{venv_activate_script}"'
subprocess.run(activate_command, shell=True, executable=r'C:\WINDOWS\system32\cmd.exe')

# Strip newline characters from the test paths
test_paths = [path.strip() for path in test_paths]

# Parameters for the py.test command
hostname = hosts.LADBROKES_BETA
browser_stack_device = BS_Devices.SAMSUNG_GALAXY_S8_ANDROID_V7_0_ANDROID
# Set environment variables before executing the command
env = os.environ.copy()
# Loop through each test path and run the py.test command

for test_path in test_paths:
    command = f"py.test C:/Automation/lcg_uat/{test_path} --hostname={hostname} -v --junit-xml=results.xml --browser_stack_device={browser_stack_device} --environment=tst2 --device_name=''"
    subprocess.run(command, shell=True, env=env, executable=r'C:\WINDOWS\system32\cmd.exe')

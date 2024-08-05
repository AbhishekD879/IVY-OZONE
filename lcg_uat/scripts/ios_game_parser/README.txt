Note: Before execute Game Parser script please understand that script was written and tested under Mac OS X only.

Python configuration

1. Download python using https://www.python.org/downloads/
2. After installation of python update system path using 'Update Shell Profile.command' script. This script located in '/Application/python3.x/Update Shell Profile.command' depends on the python version
3. Make sure OS properly see installed python using commands 'which python3' and 'which pip3', also version of installed python can be verified with command 'python3 --version', it should be same as downloaded
4. Install all needed requirements using command 'pip3 install -r requirements.txt'. Warnings that pip version is outdated can be ignored.


Script configuration

Script has settings that can be configured.
1. 'INPUT_FOLDER_NAME' - Path to the source folder with game files. Default value - 'input/'
2. 'OUTPUT_FOLDER_NAME' - Path to the destination folder with game files. Default value - 'output/'
3. 'XLSX_FILE_NAME' - Path to the .xlsx document. Default value - 'rules.xlsx'
4. 'XLSX_FILE_CORAL_PAGE' - Coral page name in .xlsx document. Default value - 'Coral'
5. 'XLSX_FILE_LADBROKES_PAGE' - Ladbrokes page name in .xlsx document. Default value - 'Ladbrokes'
6. 'CORAL_GAMES_NAME' - Folder name to place Coral only games. Default value - 'Coral'
7. 'LADBROKES_GAMES_NAME' - Folder name to place Ladbrokes only games. Default value - 'Ladbrokes'
8. 'SHARED_GAMES_NAME' - Folder name to place Shared (both Coral/Ladbrokes) games. Default value - 'Shared games'
9. 'SUPPORTED_GAME_DEVELOPERS' - dictionary that contains relationship between Game Provider from .xlsx document and his folder name that contains games, where dict key - Game Provider always in lowercase and it's value - folder name
10. 'GAMES_NAMES_WITH_SPECIFIC_FORMAT' - dictionary that contains specific game files formats for different Gave Providers.


Script execution

Make sure script is placed with input/output folders on the same level.
Script can be executed using command 'python3 path_to_script/game_parser.py'

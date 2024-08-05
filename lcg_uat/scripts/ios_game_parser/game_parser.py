import os
from shutil import copyfile

import pandas as pd

INPUT_FOLDER_NAME = 'input/'
OUTPUT_FOLDER_NAME = 'output/'

XLSX_FILE_NAME = 'rules.xlsx'
XLSX_FILE_CORAL_PAGE = 'Coral'
XLSX_FILE_LADBROKES_PAGE = 'Ladbrokes'

CORAL_GAMES_NAME = 'Coral'
LADBROKES_GAMES_NAME = 'Ladbrokes'
SHARED_GAMES_NAME = 'Shared games'


SUPPORTED_GAME_DEVELOPERS = {  # in format 'game_developer': 'folder_name', game_developer always lower
    'blueprint': 'blueprint',
    'coral': 'coral',
    'games studio': '',
    'igt': 'igt',
    'netent': 'netent',
    'novomatic': 'novomatic',
    'nyx': 'nyx',
    'play\'n go': 'playngo',
    'pragmatic play': 'pragmaticplay',
    'realistic': 'realistic',
    'yggdrasil': 'yggdrasil'
}


GAMES_NAMES_WITH_SPECIFIC_FORMAT = {  # in format - game_developer (lower): name_format
    'nyx': f'{0}-ios.zip'
}


def copy_file_if_possible(from_path: str, to_path: str):
    """
    This functions copies file from specified path to the specified path.

    :param from_path: Source path of file
    :param to_path: Destination path of file
    """
    if not os.path.exists(from_path):
        print(f'File "{from_path}" does not exist, skipping...')
        return
    if os.path.exists(to_path):
        print(f'File "{to_path}" already exists, skipping...')
        return

    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    copyfile(from_path, to_path)


class ExcelFileRow:
    """This class represents single row in .xlsx document"""

    def __init__(self, data: list):
        self.brand = data[0].strip()
        self.table_type_id = data[1]  # 'Table Type ID' goes as int, not string
        self.game_variant = data[2].strip()
        self.game_name = data[3].strip()
        self.game_developer = data[4].strip()

    def __str__(self):
        """
        To make debug more readable
        """
        output = "| "
        for _, var in vars(self).items():
            output += ' ' + str(var) + ' |'
        return output


def parse_xlsx_page(xlsx_document: str, page_name: str) -> list:
    """
    This function parses specified page number of specified .xlsx document.

    :param xlsx_document: Specified .xlsx document
    :param page_name: Name of page in .xlsx document
    :return: Parsed information present as list of ExcelFileRow
    """
    xlsx_file = pd.ExcelFile(xlsx_document)
    parsed_page = xlsx_file.parse(page_name)
    rules = []
    for row in parsed_page.values:
        file_row = ExcelFileRow(list(row))
        rules.append(file_row)

    return rules


def get_path_of_game(start_path: str, game_name: str):
    """
    This function gets full path of game file

    :param start_path: root folder path to start search
    :param game_name: game file name
    :return: Found path in format 'input/coral/some_game.zip'
    """
    for root, subdirs, files in os.walk(start_path):
        if game_name in files:
            return os.path.join(root, game_name)
    return None


def get_path_of_game_with_specific_name(start_path: str, game_name_format: str):
    """
    This function gets full path of game file for cases when file name can be fully defined

    :param start_path: root folder path to start search
    :param game_name_format: game file name e.g. kingdomprince-ios.zip
    :return: Found path in format 'input/coral/123-some-data-kingdomprince-ios.zip'
    """
    for root, subdirs, files in os.walk(start_path):
        for file_name in files:
            if game_name_format in file_name:
                return os.path.join(root, file_name)
    return None


def get_games_information(coral_rules, ladbrokes_rules) -> dict:
    """
    Collects all information for each game.

    :param coral_rules: Coral page of .xlsx file
    :param ladbrokes_rules: Ladbrokes page of .xlsx file
    :return: Collected games information as dict in view
            {
            'game_name':
                {
                    'destination_brand': 'Shared'/'Coral'/'Ladbrokes' etc,
                    'game_developer': 'Blueprint'/'Netent' etc
                }
            }
    """
    games_info = {}
    all_xlsx_games = list(set([rule.game_variant for rule in (coral_rules + ladbrokes_rules)]))
    for game in all_xlsx_games:
        game_info = {}

        coral_game_row = next((rule for rule in coral_rules if rule.game_variant == game), None)
        ladbrokes_game_row = next((rule for rule in ladbrokes_rules if rule.game_variant == game), None)
        if not coral_game_row and not ladbrokes_game_row:
            print(f'Error: script error. Game "{game}" is not present nor Coral nor Ladbrokes pages')

        game_info['destination_brand'] = SHARED_GAMES_NAME if coral_game_row and ladbrokes_game_row else \
            CORAL_GAMES_NAME if coral_game_row else LADBROKES_GAMES_NAME

        if coral_game_row and ladbrokes_game_row:
            if coral_game_row.game_developer.lower() != ladbrokes_game_row.game_developer.lower():
                print(f'Game "{game}" has different game developers for Coral/Ladbrokes pages in .xlsx file. '
                      f'Please review destination for this game manually and fix configuration in .xlsx file.')
                continue  # to skip this file at all

        row = coral_game_row if coral_game_row else ladbrokes_game_row
        game_info['game_developer'] = row.game_developer.lower()  # always lower

        games_info[game] = game_info

    return games_info


def main():
    ladbrokes_page = parse_xlsx_page(xlsx_document=XLSX_FILE_NAME,
                                     page_name=XLSX_FILE_LADBROKES_PAGE)
    coral_page = parse_xlsx_page(xlsx_document=XLSX_FILE_NAME,
                                 page_name=XLSX_FILE_CORAL_PAGE)
    games_info = get_games_information(coral_rules=coral_page,
                                       ladbrokes_rules=ladbrokes_page)
    for game_name, game_info in games_info.items():
        game_developer = game_info.get('game_developer')
        if game_developer not in SUPPORTED_GAME_DEVELOPERS:
            print(f'Game developer "{game_developer}" for game "{game_name}" is not supported. Currently support includes "{list(SUPPORTED_GAME_DEVELOPERS.keys())}". '
                  f'Please add support. Skipping...')
            continue
        game_developer_folder = SUPPORTED_GAME_DEVELOPERS.get(game_developer)

        if game_developer in GAMES_NAMES_WITH_SPECIFIC_FORMAT:
            game_format = GAMES_NAMES_WITH_SPECIFIC_FORMAT.get(game_developer)
            file_path = get_path_of_game_with_specific_name(start_path=os.path.join(INPUT_FOLDER_NAME,
                                                                                    game_developer_folder),
                                                            game_name_format=game_format.format(game_name))
        else:
            file_path = get_path_of_game(start_path=os.path.join(INPUT_FOLDER_NAME, game_developer_folder),
                                         game_name=f'{game_name}.zip')
        if not file_path:
            print(f'Cannot get input file for game "{game_name}" and game developer "{game_developer_folder}". Skipping...')
            continue

        to_path = os.path.join(OUTPUT_FOLDER_NAME, game_info.get("destination_brand"), game_developer.title(), f'{game_name}.zip')
        copy_file_if_possible(from_path=file_path, to_path=to_path)


main()

"""This module contains Test Rail suite ID's for Automation and QA's test suites"""


def test_rail_suites():
    """
    This method contains reference between automation suites and QA's suites
    :return: dict where key - is QA's suite id, and it's correspond value - automation suite ID, for example:
            - Key - 637; value - 3779, where
                - 637 is ID for QA's 'Oxygen Web Regression Package' TestRail suite
                - 3779 is ID for Automation 'Voltron Automation' TestRail suite
    """
    return {
        637: 3779,
        8095: 43740,
        73191: 73189,
        73192: 73190
    }


def test_rail_suites_based_on_folder_name():
    """
    This method contains reference between automation suites and their folder location name
    :return: dict where key - test's folder location name, and it's correspond value - automation suite ID, for example:
            - Key - tests; value - 3779, where
                - tests is test's folder location name that corresponds to the QA's 'Oxygen Web Regression Package' TestRail suite
                - 3779 is ID for Automation 'Voltron Automation' TestRail suite
    """
    return {
        'tests': 3779,
        'tests_sanity': 43740,
        'tests_grid': 73189,
        'tests_connect': 73190
    }

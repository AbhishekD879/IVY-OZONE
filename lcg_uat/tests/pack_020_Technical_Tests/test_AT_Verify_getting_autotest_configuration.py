import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.ob_smoke
@vtest
class Test_AT_Verify_getting_autotest_configuration(Common):
    """
    NAME: Verify OB configuration
    """
    keep_browser_open = True

    def test_001_check_configuration_for_football_auto_test_class(self):
        """
        DESCRIPTION: Check Autotest Configuration for "Football Auto Test" class (16291 both for coral and ladbrokes)
        EXPECTED: Autotest Configuration is valid
        """
        expected_configuration = {'displayed': True, 'active': True,
                                  'live_serv_updates': True, 'cashout_available': True}

        configuration = self.ob_config.get_autotest_class(self.ob_config.football_config.autotest_class.class_id)
        self.assertEqual(configuration, expected_configuration,
                         msg=f'"Football Auto Test" class configuration "{configuration}" does'
                             f' not match expected "{expected_configuration}"')

    def test_002_check_configuration_for_autotest_premier_league_type(self):
        """
        DESCRIPTION: Check Autotest Configuration for "Autotest Premier League" type (3756 both for coral and ladbrokes)
        EXPECTED: Autotest Configuration is valid
        """
        expected_configuration = {'displayed': True, 'active': True, 'min_bet': '0.01', 'max_bet': '10,000.00',
                                  'live_serv_updates': True, 'cashout_available': True}

        autotest_premier_league = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        configuration = self.ob_config.get_autotest_type(autotest_premier_league)
        self.assertEqual(configuration, expected_configuration,
                         msg=f'"Autotest Premier League" type configuration "{configuration}" does '
                             f'not match expected "{expected_configuration}"')

    def test_003_check_configuration_for_second_autotest_league_type(self):
        """
        DESCRIPTION: Check Autotest Configuration for "2. Autotest League" type (6076 both for coral and ladbrokes)
        EXPECTED: Autotest Configuration is valid
        """
        expected_configuration = {'displayed': True, 'active': True, 'min_bet': '0.01', 'max_bet': '10,000.00',
                                  'live_serv_updates': True, 'cashout_available': True}

        autotest_league2 = self.ob_config.football_config.autotest_class.autotest_league2.type_id
        configuration = self.ob_config.get_autotest_type(autotest_league2)
        self.assertEqual(configuration, expected_configuration,
                         msg=f'"2. Autotest League" type configuration "{configuration}" does '
                             f'not match expected "{expected_configuration}"')

    def test_004_check_configuration_for_special_autotest_league_type(self):
        """
        DESCRIPTION: Check Autotest Configuration for Special Autotest league type (6228 - Coral, 70338 - Ladbrokes)
        EXPECTED: Autotest Configuration is valid
        """
        special_autotest_league = self.ob_config.football_config.autotest_class.special_autotest_league.type_id
        expected_configuration = {'displayed': True, 'active': True, 'min_bet': '0.01', 'max_bet': '10,000.00',
                                  'live_serv_updates': False, 'cashout_available': True}

        configuration = self.ob_config.get_autotest_type(special_autotest_league)
        self.assertEqual(configuration, expected_configuration,
                         msg=f'"Special Autotest league" type configuration "{configuration}" '
                             f'does not match expected "{expected_configuration}"')

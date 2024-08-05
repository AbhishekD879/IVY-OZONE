import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.login
@pytest.mark.my_bets
@pytest.mark.mobile_only
@pytest.mark.bet_history_open_bets
@vtest
class Test_C16408288_Verify_My_Bets_counter_is_not_displayed_when_there_are_no_Open_bets(BaseUserAccountTest):
    """
    TR_ID: C16408288
    VOL_ID: C58626873
    NAME: Verify My Bets counter is not displayed when there are no Open bets
    DESCRIPTION: This test case verifies that My Bets counter is not displayed when there are no Open bets for user
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: * Load Oxygen/Roxanne Application
        DESCRIPTION: * Make sure to have a user who has no open bet or hasn't placed bets
        DESCRIPTION: * Make sure 'BetsCounter' config is turned on in CMS > System configurations
        DESCRIPTION: * 'My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS
        DESCRIPTION: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
        :return:
        """
        self.check_my_bets_counter_enabled_in_cms()

    def test_001_register_new_user(self):
        """
        DESCRIPTION: Register new user
        EXPECTED: New user is successfully registered
        """
        self.__class__.new_username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.new_username)

        self.__class__.username_no_bets = tests.settings.no_bet_history_user

    def test_002_check_my_bets_option_on_footer_ribbon(self):
        """
        DESCRIPTION: Check 'My bets' option on Footer Ribbon
        EXPECTED: 'My bets' option is displayed without My bets counter icon
        """
        expected_indicator = 0

        actual_indicator = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(actual_indicator, expected_indicator,
                         msg=f'Actual value indicator "{actual_indicator}" != Expected "{expected_indicator}"')

    def test_003__log_out_and_log_in_under_user_from_preconditions_repeat_step_2(self):
        """
        DESCRIPTION: * Log out and log in under user from preconditions
        DESCRIPTION: * Repeat step #2
        EXPECTED: 'My bets' option is displayed without My bets counter icon
        """
        self.site.logout()
        self.site.login(username=self.username_no_bets)
        self.test_002_check_my_bets_option_on_footer_ribbon()

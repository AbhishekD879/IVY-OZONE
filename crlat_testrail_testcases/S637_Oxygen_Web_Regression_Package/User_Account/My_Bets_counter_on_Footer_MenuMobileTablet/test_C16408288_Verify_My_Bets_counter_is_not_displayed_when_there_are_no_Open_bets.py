import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C16408288_Verify_My_Bets_counter_is_not_displayed_when_there_are_no_Open_bets(Common):
    """
    TR_ID: C16408288
    NAME: Verify My Bets counter is not displayed when there are no Open bets
    DESCRIPTION: This test case verifies that My Bets counter is not displayed when there are no Open bets for user
    DESCRIPTION: Autotest: [C58626873]
    PRECONDITIONS: * Load Oxygen/Roxanne Application
    PRECONDITIONS: * Make sure to have a user who has no open bet or hasn't placed bets
    PRECONDITIONS: * Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: * 'My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001_register_new_user(self):
        """
        DESCRIPTION: Register new user
        EXPECTED: New user is successfully registered
        """
        pass

    def test_002_check_my_bets_option_on_footer_ribbon(self):
        """
        DESCRIPTION: Check 'My bets' option on Footer Ribbon
        EXPECTED: 'My bets' option is displayed without My bets counter icon
        """
        pass

    def test_003__log_out_and_log_in_under_user_from_preconditions_repeat_step_2(self):
        """
        DESCRIPTION: * Log out and log in under user from preconditions
        DESCRIPTION: * Repeat step #2
        EXPECTED: 'My bets' option is displayed without My bets counter icon
        """
        pass

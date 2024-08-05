import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870165_Check_user_sees_message_as_Please_log_in_to_see_your_settled_bets_when_not_logged_in_to_system_and_on_Betslip__Settled_bets_section_Log_in_button_is_available(Common):
    """
    TR_ID: C44870165
    NAME: Check user sees message as 'Please log in to see your settled bets..' when not logged in to system and on Betslip -> Settled bets section. Log in button is available
    DESCRIPTION: Check user sees message as 'Please log in to see your Cashout' when not logged in to system
    DESCRIPTION: Desktop:  Navigate to 'My Bets'
    DESCRIPTION: Mobile: Navigate to 'My bets' via 'Cashout' from the Footer menu
    DESCRIPTION: Log in button is available
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobile__navigate_to_my_bets_via_cashout_from_the_footer_menulog_in_button_is_available(self):
        """
        DESCRIPTION: For mobile:  Navigate to 'My bets' via 'Cashout' from the Footer menu
        DESCRIPTION: Log in button is available
        EXPECTED: My Bets page should open with Cashout page opened by default & check the user sees message as 'Please log in to see your Cashout' when not logged in to system with Log button is available
        """
        pass

    def test_003_for_desktop__tabletsnavigate_to_my_bets_section___(self):
        """
        DESCRIPTION: For Desktop & Tablets:
        DESCRIPTION: Navigate to My Bets section -->
        EXPECTED: My Bets page should open with Cashout page opened by default & check user sees message as 'Please log in to see your Cashout' when not logged in to system with Log in button available
        """
        pass

    def test_004_tap_on_settled_bets_tab(self):
        """
        DESCRIPTION: Tap on Settled bets tab
        EXPECTED: Check 'Please login to see your Settled bets' message is displayed once the user navigates to Settled tabs.
        EXPECTED: Log in button is available
        """
        pass

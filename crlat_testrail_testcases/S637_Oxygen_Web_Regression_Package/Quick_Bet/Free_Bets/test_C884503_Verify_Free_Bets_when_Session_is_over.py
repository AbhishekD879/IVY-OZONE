import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C884503_Verify_Free_Bets_when_Session_is_over(Common):
    """
    TR_ID: C884503
    NAME: Verify Free Bets when Session is over
    DESCRIPTION: This test case verifies Free Bets when Session is over
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. In order to trigger case when the session is over, perform the next steps:
    PRECONDITIONS: * Log in to one browser tab
    PRECONDITIONS: * Duplicate tab
    PRECONDITIONS: * Log out from the second tab -> session is over in both tabs
    PRECONDITIONS: 4. User is logged in and has free bets added
    PRECONDITIONS: 5. [How to add Free bets to user`s account] [1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * 'Use Free bet' link is displayed under event name
        """
        pass

    def test_003_tap_use_free_bet_link_and_select_free_bet_from_the_pop_up(self):
        """
        DESCRIPTION: Tap "Use Free Bet" link and select Free bet from the pop-up
        EXPECTED: Free bet is selected
        """
        pass

    def test_004_make_steps_listed_in_preconditions(self):
        """
        DESCRIPTION: Make steps listed in preconditions
        EXPECTED: User session is over
        """
        pass

    def test_005_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: * 'Log out' pop-up is displayed
        EXPECTED: * Quick Bet stays opened
        EXPECTED: * 'Use Free bet' link is NOT displayed
        EXPECTED: * CMS-configured message is NOT displayed below Free bet drop-down
        """
        pass

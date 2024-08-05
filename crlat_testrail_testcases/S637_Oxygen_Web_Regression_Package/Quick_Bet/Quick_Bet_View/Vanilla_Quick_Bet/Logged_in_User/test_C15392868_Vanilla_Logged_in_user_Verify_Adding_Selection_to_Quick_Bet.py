import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C15392868_Vanilla_Logged_in_user_Verify_Adding_Selection_to_Quick_Bet(Common):
    """
    TR_ID: C15392868
    NAME: [Vanilla] [Logged in user] Verify Adding Selection to Quick Bet
    DESCRIPTION: This test case verifies adding Selection to Quick Bet
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User should be Logged in and have a positive balance
    PRECONDITIONS: * Betslip counter should be 0
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Betslip counter does NOT increase by one
        """
        pass

    def test_003_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: * Quick Bet appears at the bottom of the page
        EXPECTED: * All selection details are displayed within Quick Bet
        EXPECTED: * the Following view should be displayed for Logged in user
        EXPECTED: ![](index.php?/attachments/get/31341)
        """
        pass

import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2779917_Verify_displaying_odds_boost_button_in_Quick_Bet_for_logged_out_user(Common):
    """
    TR_ID: C2779917
    NAME: Verify displaying odds boost button in Quick Bet for logged out user
    DESCRIPTION: This test case verifies that odds boost button displaying in Quickbet for logged out user
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Quickbet is enabled
    PRECONDITIONS: Load application
    PRECONDITIONS: Do NOT login
    """
    keep_browser_open = True

    def test_001_add_selection_with_odds_boost_availableverify_that_quick_bet_popup_is_shown_without_boost_button(self):
        """
        DESCRIPTION: Add selection with odds boost available
        DESCRIPTION: Verify that Quick Bet popup is shown WITHOUT 'BOOST' button
        EXPECTED: - Quick Bet popup is shown
        EXPECTED: - 'BOOST' button is NOT shown in Quickbet
        """
        pass

import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2600895_Verify_showing_odds_boost_section_on_bet_receipt_when_the_bet_was_placed_with_odds_boost_Single_selection(Common):
    """
    TR_ID: C2600895
    NAME: Verify showing odds boost section on bet receipt when the bet was placed with odds boost (Single selection)
    DESCRIPTION: This test case verifies that 'This bet has been boosted' text with boost icon is shown on bet receipt in case the bet was placed with odds boost for Single selection
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add Selection with Odds Boost available to the Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslip_and_tap_boost_button(self):
        """
        DESCRIPTION: Navigate to Betslip and tap 'BOOST' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/total potential returns are shown
        """
        pass

    def test_002_add_stake_and_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Add Stake and tap 'Place Bet' button
        DESCRIPTION: Verify that bet receipt is shown
        EXPECTED: Bet receipt is shown with the following elements:
        EXPECTED: - boost icon
        EXPECTED: - hardcoded text: "This bet has been boosted!"
        EXPECTED: - boost odds was taken by the user
        EXPECTED: - potential returns/total potential returns appropriate to boosted odds
        """
        pass

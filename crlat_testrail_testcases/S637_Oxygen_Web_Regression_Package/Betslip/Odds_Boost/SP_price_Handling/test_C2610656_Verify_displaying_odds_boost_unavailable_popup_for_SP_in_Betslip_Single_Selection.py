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
class Test_C2610656_Verify_displaying_odds_boost_unavailable_popup_for_SP_in_Betslip_Single_Selection(Common):
    """
    TR_ID: C2610656
    NAME: Verify displaying odds boost unavailable popup for SP in Betslip (Single Selection)
    DESCRIPTION: This test case verifies that odds boost button is not shown for SP in Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application and Login into the application
    PRECONDITIONS: Add selection with SP only available
    """
    keep_browser_open = True

    def test_001_navigate_to_betslip_and_add_a_stakeverify_that_the_odds_boost_section_is_not_shown_in_the_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip and add a stake
        DESCRIPTION: Verify that the Odds Boost section is NOT shown in the Betslip
        EXPECTED: - 'BOOST' button is NOT shown
        EXPECTED: - SP odds is shown
        """
        pass

    def test_002_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that Bet Receipt is shown
        EXPECTED: Bet Receipt is shown with SP odds
        """
        pass

    def test_003_add_selection_with_lp_and_sp_available_lp_is_selectednavigate_to_betslip_and_add_a_stake_to_the_selectionverify_that_the_odds_boost_section_is_shown_in_the_betslip(self):
        """
        DESCRIPTION: Add selection with LP and SP available (LP is selected)
        DESCRIPTION: Navigate to Betslip and add a Stake to the selection
        DESCRIPTION: Verify that the Odds Boost section is shown in the Betslip
        EXPECTED: Odds Boost section is shown on the top of Betslip with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon
        """
        pass

    def test_004_tap_a_boost_button(self):
        """
        DESCRIPTION: Tap a 'BOOST' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed in dropdown
        EXPECTED: - Updated (to reflect the boosted odds) potential returns are shown
        """
        pass

    def test_005_change_lp_to_spverify_that_odds_boost_popup_is_shown(self):
        """
        DESCRIPTION: Change LP to SP
        DESCRIPTION: Verify that Odds Boost popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - hardcoded 'Odds Boost Unavailable' title
        EXPECTED: - hardcoded 'Odds Boost is unavailable for SP selection' message text
        EXPECTED: - 'OK' button
        """
        pass

    def test_006_tap_ok_buttonverify_that_odds_boost_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that Odds boost popup is closed
        EXPECTED: - The popup is closed
        EXPECTED: - Odds boost button is de-selected ('BOOST' button is shown)
        EXPECTED: - SP price is shown
        EXPECTED: - N/A is shown Est. Returns
        """
        pass

    def test_007_tap_boost_button_one_more_timeverify_that_odds_boost_popup_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button one more time
        DESCRIPTION: Verify that Odds boost popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - hardcoded 'Odds Boost Unavailable' title
        EXPECTED: - hardcoded 'Odds Boost is unavailable for SP selection' message text
        EXPECTED: - 'OK' button
        """
        pass

    def test_008_tap_ok_buttonverify_that_odds_boost_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that Odds boost popup is closed
        EXPECTED: - The popup is closed
        EXPECTED: - Odds boost button is NOT selected to the boosted state ('BOOST' button is shown)
        EXPECTED: - SP price is shown
        EXPECTED: - N/A is shown for Est. Returns
        """
        pass

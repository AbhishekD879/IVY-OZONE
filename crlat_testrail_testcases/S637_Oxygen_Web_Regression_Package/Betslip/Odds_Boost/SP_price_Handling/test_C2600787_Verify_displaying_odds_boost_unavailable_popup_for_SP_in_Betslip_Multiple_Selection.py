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
class Test_C2600787_Verify_displaying_odds_boost_unavailable_popup_for_SP_in_Betslip_Multiple_Selection(Common):
    """
    TR_ID: C2600787
    NAME: Verify displaying odds boost unavailable popup for SP in Betslip (Multiple Selection)
    DESCRIPTION: This test case verifies that a clear message that Odds Boost is not available for SP Bets is showing in Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application and Login into the application
    PRECONDITIONS: Add selection with SP only available (Selection_1)
    PRECONDITIONS: Add selection with LP and SP available (Selection_2) and LP price is selected
    PRECONDITIONS: Add selection with LP and SP available (Selection_3) and LP price is selected
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipverify_that_the_odds_boost_section_is_shown_in_the_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that the Odds Boost section is shown in the Betslip
        EXPECTED: Odds Boost section is shown on the top of Betslip with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon (tooltip)
        """
        pass

    def test_002_add_stake_and_tap_a_boost_button(self):
        """
        DESCRIPTION: Add Stake and tap a 'BOOST' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED'
        EXPECTED: - 'i' icon is shown for Selection_1
        EXPECTED: - Boosted odds is NOT shown for Selection_1
        EXPECTED: - Boosted odds is shown for Section_2 and Selection_3
        EXPECTED: - Original odds is displayed for Selection_2 and Selection_3 in dropdown
        EXPECTED: - N/A is shown Returns
        """
        pass

    def test_003_tap_i_icon_for_selection_1verify_that_notification_is_shown(self):
        """
        DESCRIPTION: Tap 'i' icon for Selection_1
        DESCRIPTION: Verify that notification is shown
        EXPECTED: Notification is displayed with the hardcoded text: 'Odds Boost is unavailable for this selection'
        """
        pass

    def test_004_change_lp_to_sp_for_selection_2verify_that_odds_boost_popup_is_shown(self):
        """
        DESCRIPTION: Change LP to SP for Selection_2
        DESCRIPTION: Verify that Odds Boost popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - hardcoded 'Odds Boost Unavailable' title
        EXPECTED: - hardcoded 'Odds Boost is unavailable for SP selection' message text
        EXPECTED: - 'OK' button
        """
        pass

    def test_005_tap_ok_buttonverify_that_odds_boost_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that Odds boost popup is closed
        EXPECTED: - The popup is closed
        EXPECTED: - Odds boost button is de-selected ('BOOST' button is shown)
        EXPECTED: - 'i' icon is NOT shown for Selection_1
        EXPECTED: - SP price is shown for Selection_1 and Selection_2
        EXPECTED: - Selection_3 is rolled back to an UNboosted state
        EXPECTED: - N/A is shown for returns
        """
        pass

    def test_006_tap_boost_button_one_more_timeverify_that_odds_boost_popup_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button one more time
        DESCRIPTION: Verify that Odds boost popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - hardcoded 'Odds Boost Unavailable' title
        EXPECTED: - hardcoded 'Odds Boost is unavailable for SP selection' message text
        EXPECTED: - 'OK' button
        """
        pass

    def test_007_tap_ok_buttonverify_that_odds_boost_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that Odds boost popup is closed
        EXPECTED: - The popup is closed
        EXPECTED: - Odds boost button is NOT selected to the boosted state
        EXPECTED: - 'i' icon is NOT shown for Section_1
        EXPECTED: - SP price is shown for Selection_1 and Selection_2
        EXPECTED: - Selection_3 is shown in an UNboosted state
        EXPECTED: - N/A is shown for returns
        """
        pass

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
class Test_C2693980_Verify_Odds_Boost_unavailable_pop_up_for_SP_in_Quickbet(Common):
    """
    TR_ID: C2693980
    NAME: Verify Odds Boost unavailable pop up for SP in Quickbet
    DESCRIPTION: This test case verifies Odds Boost unavailable pop up for SP in Quickbet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application
    """
    keep_browser_open = True

    def test_001_add_a_selection_to_the_quickbet_with_lp_and_sp_available(self):
        """
        DESCRIPTION: Add a selection to the Quickbet with LP and SP available
        EXPECTED: Selection is added to the Quickbet
        EXPECTED: Odds Boost section is available
        """
        pass

    def test_002_tap_boost_buttonverify_that_odds_is_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds is boosted
        EXPECTED: - 'BOOST' button changed to 'BOOSTED'
        EXPECTED: - Original odds is shown in dropdown
        EXPECTED: - New boosted adds is shown
        """
        pass

    def test_003_change_lp_to_spverify_that_odds_boost_unavailable_popup_is_shown(self):
        """
        DESCRIPTION: Change LP to SP
        DESCRIPTION: Verify that Odds Boost unavailable popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - 'Odds Boost is unavailable for SP selections.' - hardcoded text is displayed
        EXPECTED: - 'Odds Boost unavailable' - the hardcoded header text is displayed
        EXPECTED: - 'OK' button is displayed
        """
        pass

    def test_004_verify_that_popup_is_closable_by_tapping_ok_or_anywhere(self):
        """
        DESCRIPTION: Verify that popup is closable by tapping 'OK' or anywhere
        EXPECTED: - Pop up is closed
        EXPECTED: - SP price is shown for selection
        EXPECTED: - The Odds boost button is de-selected back to an unboosted state
        EXPECTED: - Boosted price is rolled back to an unboosted state
        EXPECTED: - Odds boost button is tappable
        """
        pass

    def test_005_tap_boost_button(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        EXPECTED: The same Odds boost unavailable popup is displayed with the following elements:
        EXPECTED: - 'Odds Boost is unavailable for SP selections.' - hardcoded text is displayed
        EXPECTED: - 'Odds Boost unavailable' - the hardcoded header text is displayed
        EXPECTED: - 'OK' button is displayed
        """
        pass

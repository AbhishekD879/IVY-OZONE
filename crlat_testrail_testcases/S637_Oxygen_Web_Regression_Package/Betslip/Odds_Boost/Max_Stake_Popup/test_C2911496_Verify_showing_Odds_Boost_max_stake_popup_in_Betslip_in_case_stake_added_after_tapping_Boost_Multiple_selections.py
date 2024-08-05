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
class Test_C2911496_Verify_showing_Odds_Boost_max_stake_popup_in_Betslip_in_case_stake_added_after_tapping_Boost_Multiple_selections(Common):
    """
    TR_ID: C2911496
    NAME: Verify showing Odds Boost max stake popup in Betslip in case stake added after tapping Boost (Multiple selections)
    DESCRIPTION: This test case verifies that odds boost max stake popup is showing when BOOST button is tapped and then stake is added for multiple selections
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: CREATE and ADD Odds Boost tokens for USER1, where max redemption value = 50, use instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add TWO selections with appropriate odds boost available to Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: BOOST button is shown
        """
        pass

    def test_002_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: - Boosted odds is shown for SINGLES and DOUBLE
        EXPECTED: - Original odds is shown as cross out for SINGLES and DOUBLE
        """
        pass

    def test_003_add_a_stakes__for_selections_that_will_be_lower_or_equal_to_max_redemption_value__50__50single1__12single2__18double__20verify_that_max_stake_popup_is_not_shown(self):
        """
        DESCRIPTION: Add a Stakes  for selections that will be lower or equal to max redemption value ( 50 = 50):
        DESCRIPTION: Single1 = 12
        DESCRIPTION: Single2 = 18
        DESCRIPTION: Double = 20
        DESCRIPTION: Verify that max stake popup is NOT shown
        EXPECTED: - Popup is NOT shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is shown as cross out
        """
        pass

    def test_004_add_one_more_selection_with_appropriate_odds_boost_availableenter_stake_value_for_the_selection_stake__1_and_treble__21verify_that_max_stake_popup_is_shown(self):
        """
        DESCRIPTION: Add one more selection with appropriate odds boost available
        DESCRIPTION: Enter stake value for the selection (Stake = 1 and TREBLE = 21)
        DESCRIPTION: Verify that max stake popup is shown
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: - the hardcoded text:'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake.' You can boost up to 50 (the max redemption value defined in the token in TI by default) of your total stake
        EXPECTED: - OK button
        """
        pass

    def test_005_tap_ok_buttonverify_that_popup_is_closed_and_odds_boost_is_deselected(self):
        """
        DESCRIPTION: Tap OK button
        DESCRIPTION: Verify that popup is closed and odds boost is deselected
        EXPECTED: - Popup is closed
        EXPECTED: - BOOST button is shown
        EXPECTED: - Odds is NOT boosted
        """
        pass

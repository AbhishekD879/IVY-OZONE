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
class Test_C2911495_Verify_showing_Odds_Boost_max_stake_popup_in_Betslip_in_case_stake_added_before_tapping_Boost_Multiple_selections(Common):
    """
    TR_ID: C2911495
    NAME: Verify showing Odds Boost max stake popup in Betslip in case stake added before tapping Boost (Multiple selections)
    DESCRIPTION: This test case verifies that odds boost max stake popup is showing when stake is added and then BOOST button is tapped for multiple selections
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: CREATE and ADD Odds Boost tokens for USER1, where max redemption value = 50, use instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add TWO selections with appropriate odds boost available to Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipadd_a_stakes_for_selections_that_will_be_higher_as_max_redemption_value__5150single1__12single2__18double__21verify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Add a Stakes for selections that will be higher as max redemption value ( 51>50):
        DESCRIPTION: Single1 = 12
        DESCRIPTION: Single2 = 18
        DESCRIPTION: Double = 21
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: BOOST button is shown
        """
        pass

    def test_002_tap_boost_buttonverify_that_max_stake_popup_is_shown(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that max stake popup is shown
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: - the hardcoded text:'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake.' You can boost up to 50 (the max redemption value defined in the token in TI by default) of your total stake
        EXPECTED: - OK button
        """
        pass

    def test_003_tap_anywhere_out_of_popupverify_that_popup_is_closed_and_odds_are_not_boosted(self):
        """
        DESCRIPTION: Tap anywhere out of popup
        DESCRIPTION: Verify that popup is closed and odds are NOT boosted
        EXPECTED: - Popup is closed
        EXPECTED: - BOOST button is shown
        EXPECTED: - Odds is NOT boosted
        """
        pass

    def test_004_edit_stakes_to_make_the_sum_of_them_lower_or_equal_then_max_redemption_value_50__50_single1__12single2__17double__21verify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Edit stakes to make the sum of them lower or equal then max redemption value (50 = 50) :
        DESCRIPTION: Single1 = 12
        DESCRIPTION: Single2 = 17
        DESCRIPTION: Double = 21
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: BOOST button is shown
        """
        pass

    def test_005_tap_boost_buttonverify_that_max_stake_popup_is_not_shown(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that max stake popup is NOT shown
        EXPECTED: - Popup is NOT shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is shown as cross out
        """
        pass

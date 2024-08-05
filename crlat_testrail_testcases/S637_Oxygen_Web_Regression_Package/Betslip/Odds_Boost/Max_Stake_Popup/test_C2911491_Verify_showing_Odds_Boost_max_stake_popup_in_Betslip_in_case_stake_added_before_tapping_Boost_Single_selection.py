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
class Test_C2911491_Verify_showing_Odds_Boost_max_stake_popup_in_Betslip_in_case_stake_added_before_tapping_Boost_Single_selection(Common):
    """
    TR_ID: C2911491
    NAME: Verify showing Odds Boost max stake popup in Betslip in case stake added before tapping Boost (Single selection)
    DESCRIPTION: This test case verifies that odds boost max stake popup is showing when stake is added and then BOOST button is tapped
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: CREATE and ADD Odds Boost tokens for USER1, where max redemption value = 50, use instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add selection with appropriate odds boost available to Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipadd_a_stake_value_higher_then_max_redemption_value_stake_value__51verify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Add a Stake value higher then max redemption value (Stake value = 51)
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: BOOST button  is shown
        """
        pass

    def test_002_tap_boost_buttonverify_that_max_stake_popup_is_shown(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that max stake popup is shown
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: -  the hardcoded text:'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake.' You can boost up to 50 (the max redemption value defined in the token in TI by default) of your total stake
        EXPECTED: - OK button
        """
        pass

    def test_003_tap_ok_buttonverify_that_popup_is_closed_and_odds_is_not_boosted(self):
        """
        DESCRIPTION: Tap OK button
        DESCRIPTION: Verify that popup is closed and odds is NOT boosted
        EXPECTED: - Popup is closed
        EXPECTED: - BOOST button is shown
        EXPECTED: - Odds is NOT boosted
        """
        pass

    def test_004_edit_stake__and_set_it_equal_to_the_max_redemption_value_stake_value__50verify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Edit Stake  and set it equal to the max redemption value. (Stake value = 50)
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

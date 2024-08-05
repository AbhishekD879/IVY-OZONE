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
class Test_C2911499_Verify_displaying_Odds_Boost_max_stake_popup_in_Quick_Bet_in_case_stake_is_added_after_tapping_Boost_button(Common):
    """
    TR_ID: C2911499
    NAME: Verify displaying Odds Boost max stake popup in Quick Bet in case stake is added after tapping Boost button
    DESCRIPTION: This test case verifies displaying Odds Boost max stake popup in Quick Bet in case stake above the token max stake is added after tapping Boost button
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Create and Add Odds Boost token to the user, where max redemption value = 50 (50 is set by default, we cannot change it)
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    PRECONDITIONS: Add selection with appropriate odds boost available to Quickbet
    """
    keep_browser_open = True

    def test_001_tap_boost_button(self):
        """
        DESCRIPTION: Tap 'Boost' button
        EXPECTED: - 'Boost' button is enabled
        EXPECTED: - Boosted odds is shown
        """
        pass

    def test_002_add_stake_stake__50_or_lessverify_that_max_stake_popup_is_not_shown(self):
        """
        DESCRIPTION: Add Stake (Stake = 50 or less)
        DESCRIPTION: Verify that max stake popup is NOT shown
        EXPECTED: - Popup is NOT shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Total Stake and Potential returns are updated
        """
        pass

    def test_003_edit_stake_stake51_or_moreverify_that_max_stake_popup_is_shown(self):
        """
        DESCRIPTION: Edit Stake (Stake=51 or more)
        DESCRIPTION: Verify that Max stake popup is shown
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: - the hardcoded text:'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake.' You can boost up to 50 of your total stake
        EXPECTED: - OK button
        """
        pass

    def test_004_verify_that_popup_is_closable_by_ok_or_tapping_anywhere(self):
        """
        DESCRIPTION: Verify that popup is closable by 'OK' or tapping anywhere
        EXPECTED: Popup is closed
        """
        pass

    def test_005_verify_that_odds_boost_is_deselected(self):
        """
        DESCRIPTION: Verify that odds boost is deselected
        EXPECTED: The Boost is deselected
        """
        pass

    def test_006_reduce_the_stake_amount_to_appropriate_value_50_or_less__tap_boost_button(self):
        """
        DESCRIPTION: Reduce the stake amount to appropriate value (50 or less) & tap 'Boost' button
        EXPECTED: - Stake is successfully boosted
        EXPECTED: - Popup is NOT shown
        EXPECTED: - Total Stake and Potential returns are updated
        """
        pass

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
class Test_C2911494_Verify_displaying_Odds_Boost_max_stake_popup_in_Quick_bet_in_case_if_stake_was_added_before_tapping_Boost(Common):
    """
    TR_ID: C2911494
    NAME: Verify displaying Odds Boost max stake popup in Quick bet in case if stake was added before tapping Boost
    DESCRIPTION: This test case verifies that Odds Boost max stake popup is displaying when stake is added and then BOOST button is tapped
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Create and Add Odds Boost token to the user, where max redemption value = 50 (50 is set by default)
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    PRECONDITIONS: Add selection with appropriate odds boost available to Quickbet
    """
    keep_browser_open = True

    def test_001_enter_a_stake_above_the_max_redemption_value_stake_51_or_more(self):
        """
        DESCRIPTION: Enter a stake above the max redemption value (Stake =51 or more)
        EXPECTED: Stake is placed
        EXPECTED: Boost button is available
        """
        pass

    def test_002_tap_boost_button_and_verify_that_max_stake_popup_message_is_displayed(self):
        """
        DESCRIPTION: Tap 'Boost' button and verify that Max stake popup message is displayed
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: - the hardcoded text:'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake.' You can boost up to 50 of your total stake
        EXPECTED: - OK button
        """
        pass

    def test_003_verify_that_popup_is_closable_by_ok_or_tapping_anywhere(self):
        """
        DESCRIPTION: Verify that popup is closable by 'OK' or tapping anywhere
        EXPECTED: Popup is closed
        """
        pass

    def test_004_verify_that_the_boost_is_deselected_after_popup_was_closed(self):
        """
        DESCRIPTION: Verify that the boost is deselected after popup was closed
        EXPECTED: The boost is deselected
        """
        pass

    def test_005_reduce_the_stake_amount_to_appropriate_value_50_or_less__tap_boost_button(self):
        """
        DESCRIPTION: Reduce the stake amount to appropriate value (50 or less) & tap 'Boost' button
        EXPECTED: Stake is successfully boosted
        """
        pass

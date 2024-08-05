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
class Test_C2605931_Verify_displaying_odds_boost_button_in_Quick_Bet_for_logged_in_user(Common):
    """
    TR_ID: C2605931
    NAME: Verify displaying odds boost button in Quick Bet for logged in user
    DESCRIPTION: This test case verifies that odds boost button displaying in Quickbet for logged in user
    DESCRIPTION: Autotest [C2605931]
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Quickbet is enabled
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Fractional odds selected for User1
    PRECONDITIONS: Load application and do NOT login
    """
    keep_browser_open = True

    def test_001_add_selection_with_odds_boost_availableverify_that_quick_bet_is_shown_without_boost_button(self):
        """
        DESCRIPTION: Add selection with odds boost available
        DESCRIPTION: Verify that Quick Bet is shown WITHOUT 'BOOST' button
        EXPECTED: 'BOOST' button is not shown
        """
        pass

    def test_002_login_with_user1add_selection_with_odds_boost_availableverify_that_quick_bet_is_shown_with_boost_button(self):
        """
        DESCRIPTION: Login with User1
        DESCRIPTION: Add selection with odds boost available
        DESCRIPTION: Verify that Quick Bet is shown WITH 'BOOST' button
        EXPECTED: Quick Bet is shown
        EXPECTED: 'BOOST' button is shown in Quick Bet
        EXPECTED: ![](index.php?/attachments/get/31378)
        EXPECTED: ![](index.php?/attachments/get/31377)
        """
        pass

    def test_003_add_stake_and_tap_boost_buttonverify_that_odds_boost_button_is_shown_with_animation_and_the_odds_are_boosted(self):
        """
        DESCRIPTION: Add Stake and tap 'BOOST' button
        DESCRIPTION: Verify that odds boost button is shown with animation and the odds are boosted
        EXPECTED: Quick Bet is displayed with the following elements:
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        EXPECTED: ![](index.php?/attachments/get/31380)
        EXPECTED: ![](index.php?/attachments/get/31379)
        """
        pass

    def test_004_tap_boosted_buttonverify_that_odds_boost_button_is_shown_with_animation_and_the_odds_boost_is_removed(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost button is shown with animation and the odds boost is removed
        EXPECTED: - 'BOOSTED' button is changed to 'BOOST' button with animation
        EXPECTED: - Original odds (fractional) is shown
        EXPECTED: - Boosted odds is removed
        EXPECTED: - Returns are rolled back
        """
        pass

    def test_005_tap_boost_button_one_more_timeverify_that_odds_boost_button_is_shown_with_animation_and_the_odds_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button one more time
        DESCRIPTION: Verify that odds boost button is shown with animation and the odds are boosted
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        pass

    def test_006_tap_add_to_betslip_button_and_navigate_to_betslipverify_that_boosted_odds_is_shown_in_betslip(self):
        """
        DESCRIPTION: Tap 'Add to Betslip' button and navigate to Betslip
        DESCRIPTION: Verify that BOOSTED odds is shown in Betslip
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOSTED' button
        EXPECTED: - Boosted odds (fractional)
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns
        """
        pass

    def test_007_remove_selection_from_betslip_and_add_it_one_more_time_to_quick_betverify_that_quick_bet_is_shown_with_boost_button(self):
        """
        DESCRIPTION: Remove selection from Betslip and add it one more time to Quick bet
        DESCRIPTION: Verify that Quick Bet is shown WITH 'BOOST' button
        EXPECTED: Quick Bet is shown
        EXPECTED: 'BOOST' button is shown in Quick Bet
        """
        pass

    def test_008_change_odds_format_to_decimalverify_that_this_functionality_works_the_same_with_decimal_odds(self):
        """
        DESCRIPTION: Change odds format to Decimal
        DESCRIPTION: Verify that this functionality works the same with decimal odds
        EXPECTED: - Boosted odds is shown in decimal
        EXPECTED: - Original odds is displayed as crossed out in decimal
        """
        pass

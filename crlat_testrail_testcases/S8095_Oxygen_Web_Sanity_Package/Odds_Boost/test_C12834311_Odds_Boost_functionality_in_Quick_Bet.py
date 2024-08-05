import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C12834311_Odds_Boost_functionality_in_Quick_Bet(Common):
    """
    TR_ID: C12834311
    NAME: Odds Boost functionality in Quick Bet
    DESCRIPTION: This test case verifies  Odds Boost functionality in Quick Bet
    DESCRIPTION: AUTOTEST [C50985241] TST2 ONLY
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Quick Bet is enabled
    PRECONDITIONS: Generate for user Odds boost token with ANY token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add OB token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Note: Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Load application and do NOT log in
    PRECONDITIONS: Fractional odds format selected for User1
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_quick_bet_and_verify_that_quick_bet_is_shown_without_boost_button(self):
        """
        DESCRIPTION: Add selection to the Quick Bet and verify that Quick Bet is shown WITHOUT 'BOOST' button
        EXPECTED: - Quick Bet is shown
        EXPECTED: - 'BOOST' button is NOT shown in Quick Bet
        """
        pass

    def test_002_close_quick_bet_and_login_into_application_with_a_user1_that_has_an_odds_boost_token(self):
        """
        DESCRIPTION: Close Quick Bet and Login into Application with a User1 that has an Odds Boost token
        EXPECTED: - User is logged in successfully
        EXPECTED: - The "Odds Boost" token notification is displayed
        """
        pass

    def test_003_add_selection_that_is_applicable_for_odds_boost_into_the_quick_bet(self):
        """
        DESCRIPTION: Add selection that is applicable for Odds Boost into the Quick Bet
        EXPECTED: - Quick Bet is shown
        EXPECTED: - 'BOOST' button is available in Quick Bet
        EXPECTED: ![](index.php?/attachments/get/11126186)
        EXPECTED: ![](index.php?/attachments/get/11126187)
        """
        pass

    def test_004_add_stake_to_the_selection_and_tap_boost_button(self):
        """
        DESCRIPTION: Add 'Stake' to the selection and tap 'BOOST' button
        EXPECTED: Quick Bet is displayed with the following elements:
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button
        EXPECTED: - Boosted odds are shown near original odds in a (yellow or dark blue depending on a brand) frame
        EXPECTED: - Original odds are displayed as crossed out on the left side of the boosted odds
        EXPECTED: - Updated (to reflect the boosted odds) Estimated/('Total' for **PRE OX 99**) Potential Returns are shown
        EXPECTED: ![](index.php?/attachments/get/11199564)
        EXPECTED: ![](index.php?/attachments/get/11200757)
        """
        pass

    def test_005_tap_boosted_buttonverify_that_odds_boost_button_is_shown_with_animation_and_the_odds_boost_is_removed(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost button is shown with animation and the odds boost is removed
        EXPECTED: - 'BOOSTED' button is changed to 'BOOST' button with animation
        EXPECTED: - Original odds are shown
        EXPECTED: - Boosted odds are removed
        EXPECTED: - Estimated/('Total' for **PRE OX 99**) Potential Returns are rolled back to match calculations for the original odds
        """
        pass

    def test_006_tap_boost_button_one_more_time_and_then_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button one more time and then tap 'Place Bet' button.
        DESCRIPTION: Verify that bet receipt is shown
        EXPECTED: Bet receipt is shown with the following elements:
        EXPECTED: - Boost icon
        EXPECTED: - Hardcoded text: "This bet has been boosted!"
        EXPECTED: - boosted odds are shown as those used for bet placement
        EXPECTED: - Estimated/('Total' for **PRE OX 99**) Potential Returns match calculations for boosted odds
        """
        pass

    def test_007_provide_same_verifications_with_decimal_odds_format(self):
        """
        DESCRIPTION: Provide same verifications with decimal odds format
        EXPECTED: 
        """
        pass

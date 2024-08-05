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
class Test_C2600893_Verify_showing_information_popup_when_Free_Bet_is_selected_and_then_Odds_Boost_is_selected_in_Betslip(Common):
    """
    TR_ID: C2600893
    NAME: Verify showing information popup when Free Bet is selected and then Odds Boost is selected in Betslip
    DESCRIPTION: This Test case verifies that information notification with one button is shown when Free Bet is selected and then the odds are boosted
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate for user FreeBet token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add Selection with Odds Boost available to the Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslip_and_add_one_of_the_available_free_bets_to_the_selection(self):
        """
        DESCRIPTION: Navigate to Betslip and add one of the available free bets to the selection
        EXPECTED: - The Free Bet is added
        EXPECTED: - The Odds boost section with 'BOOST' button is shown
        """
        pass

    def test_002_tap_boost_buttonverify_that_information_popup_with_one_button_is_displayed(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that information popup (with one button) is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Unfortunately you can't boost your odds while using a Free Bet. Please de-select your Free Bet to boost your odds."
        EXPECTED: - 'OK, THANKS' button
        """
        pass

    def test_003_tap_ok_thanks_buttonverify_that_popup_is_closed_and_free_bet_remains_selected(self):
        """
        DESCRIPTION: Tap 'OK, THANKS' button
        DESCRIPTION: Verify that popup is closed and free bet remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - The selected free bet remains selected
        EXPECTED: - The odds boost button remains in an unboosted state (show as BOOST)
        EXPECTED: - Odds of all selections on the betslip are rolled back to an unboosted state
        """
        pass

    def test_004_tap_place_bet_buttonverify_that_bet_is_placed_with_free_bet(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        DESCRIPTION: Verify that Bet is placed with Free Bet
        EXPECTED: The receipt with Free Bet Stake is shown
        """
        pass

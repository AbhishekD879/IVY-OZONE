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
class Test_C2708792_Verify_showing_information_popup_when_Free_Bet_is_selected_and_then_Odds_Boost_is_selected_in_Quick_Bet(Common):
    """
    TR_ID: C2708792
    NAME: Verify showing information popup when Free Bet is selected and then Odds Boost is selected in Quick Bet
    DESCRIPTION: This Test case verifies that information notification with one button is shown when Free Bet is selected and then the odds are boosted in Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate for user FreeBet token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True

    def test_001_add_selection_with_odds_boost_available_to_quick_betverify_that_quick_bet_is_shown_with_free_bets_dropdown_and_boost_button(self):
        """
        DESCRIPTION: Add selection (with odds boost available) to Quick Bet
        DESCRIPTION: Verify that Quick bet is shown with Free Bets dropdown and 'Boost' button
        EXPECTED: Quick Bet is shown with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - 'Free Bets' drop down (Before OX99)
        EXPECTED: 'Use Free Bet' button (After OX99)
        """
        pass

    def test_002_add_one_of_the_available_free_bets(self):
        """
        DESCRIPTION: Add one of the available free bets
        EXPECTED: - The Free Bet is add
        EXPECTED: - The 'BOOST' button is shown
        """
        pass

    def test_003_tap_boost_buttonverify_that_information_popup_with_one_button_is_displayed(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that information popup (with one button) is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Unfortunately you can't boost your odds while using a Free Bet. Please de-select your Free Bet to boost your odds."
        EXPECTED: - 'OK THANKS' button
        """
        pass

    def test_004_tap_ok_thanks_buttonverify_that_popup_is_closed_and_free_bet_remains_selected(self):
        """
        DESCRIPTION: Tap 'OK THANKS' button
        DESCRIPTION: Verify that popup is closed and free bet remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - The selected free bet remains selected
        EXPECTED: - The odds boost button remains in an unboosted state (show as BOOST)
        EXPECTED: - Odds of all selections in the Quick Bet are rolled back to an unboosted state
        """
        pass

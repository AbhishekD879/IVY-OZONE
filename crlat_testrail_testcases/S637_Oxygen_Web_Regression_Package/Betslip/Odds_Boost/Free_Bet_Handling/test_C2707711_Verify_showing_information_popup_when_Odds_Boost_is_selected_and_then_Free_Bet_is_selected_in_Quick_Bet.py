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
class Test_C2707711_Verify_showing_information_popup_when_Odds_Boost_is_selected_and_then_Free_Bet_is_selected_in_Quick_Bet(Common):
    """
    TR_ID: C2707711
    NAME: Verify showing information popup when Odds Boost is selected and then Free Bet is selected in Quick Bet
    DESCRIPTION: This Test case verifies that information notification with two buttons is shown when odds are boosted and then Free Bet is selected in Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate for user FreeBet token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True

    def test_001_add_selection_with_odds_boost_available_to_quick_betverify_that_quick_bet_is_shown_with_free_bets_available_and_boost_button(self):
        """
        DESCRIPTION: Add selection (with odds boost available) to Quick Bet
        DESCRIPTION: Verify that Quick bet is shown with Free Bets available and 'Boost' button
        EXPECTED: Quick Bet is opened with following elements:
        EXPECTED: - BOOST' button
        EXPECTED: - 'Free Bets' drop down (Before OX99)
        EXPECTED: 'Use Free Bet 'button (After OX99)
        """
        pass

    def test_002_tap_boost_buttonverify_that_odds_is_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds is boosted
        EXPECTED: - Button state is changed to 'Boosted'
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is shown as crossed out
        """
        pass

    def test_003_add_one_of_the_available_free_betsverify_that_information_popup_is_displayed(self):
        """
        DESCRIPTION: Add one of the available free bets
        DESCRIPTION: Verify that information popup is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: - 'NO, THANKS' button
        EXPECTED: - 'YES, PLEASE' button
        """
        pass

    def test_004_tap_no_thanks_buttonverify_that_popup_is_closed_and_odds_boost_remains_selected(self):
        """
        DESCRIPTION: Tap 'NO, THANKS' button
        DESCRIPTION: Verify that popup is closed and odds boost remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - Odds Boost button remains selected (show as BOOSTED)
        EXPECTED: - Odds is shown in boosted state
        EXPECTED: - Original odd remains cross out
        EXPECTED: - The free bet is deselected (removed)
        """
        pass

    def test_005_add_one_of_the_available_free_bets_one_more_timeverify_that_information_popup_with_two_buttons_is_displayed(self):
        """
        DESCRIPTION: Add one of the available free bets one more time
        DESCRIPTION: Verify that information popup (with two buttons) is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: - 'NO, THANKS' button
        EXPECTED: - 'YES, PLEASE' button
        """
        pass

    def test_006_tap_yes_please_buttonverify_that_popup_is_closed_and_freebet_remains(self):
        """
        DESCRIPTION: Tap 'YES, PLEASE' button
        DESCRIPTION: Verify that popup is closed and Freebet remains
        EXPECTED: - Popup is closed
        EXPECTED: - The selected free bet remains selected
        EXPECTED: - The odds boost button is rolled back to an unboosted state (show as BOOST)
        EXPECTED: - Odds of is rolled back to an unboosted state
        """
        pass

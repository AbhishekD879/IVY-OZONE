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
class Test_C2600888_Verify_showing_information_popup_when_Odds_Boost_is_selected_and_then_Free_Bet_is_selected_in_Betslip(Common):
    """
    TR_ID: C2600888
    NAME: Verify showing information popup when Odds Boost is selected and then Free Bet is selected in Betslip
    DESCRIPTION: This Test case verifies that information notification with two buttons is shown when odds are boosted and than Free Bet is selected
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Generate for user FreeBet token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add Selection with Odds Boost available to the Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslip_and_tap_boost_button(self):
        """
        DESCRIPTION: Navigate to Betslip and Tap 'BOOST' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' with animation
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is shown as crossed out
        EXPECTED: - Before OX99: Free Bet dropdown is shown
        EXPECTED: After OX99: 'Use Free Bet' button is shown
        """
        pass

    def test_002_choose_one_of_the_available_free_betsverify_that_information_popup_is_displayed(self):
        """
        DESCRIPTION: Choose one of the available free bets
        DESCRIPTION: Verify that information popup is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: - 'NO, THANKS' button
        EXPECTED: - 'YES, PLEASE' button
        """
        pass

    def test_003_tap_no_thanks_buttonverify_that_popup_is_closed_and_odds_boost_remains_selected(self):
        """
        DESCRIPTION: Tap 'NO, THANKS' button
        DESCRIPTION: Verify that popup is closed and odds boost remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - Odds Boost button remains selected (show as BOOSTED)
        EXPECTED: - Odds is shown in boosted state
        EXPECTED: - Original odds remains cross out
        EXPECTED: - The free bet is deselected (removed)
        """
        pass

    def test_004_choose_one_of_the_available_free_bets_one_more_timeverify_that_information_popup_is_displayed(self):
        """
        DESCRIPTION: Choose one of the available free bets one more time
        DESCRIPTION: Verify that information popup is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: - 'NO, THANKS' button
        EXPECTED: - 'YES, PLEASE' button
        """
        pass

    def test_005_tap_yes_please_buttonverify_that_popup_is_closed_and_freebet_remains_selected(self):
        """
        DESCRIPTION: Tap 'YES, PLEASE' button
        DESCRIPTION: Verify that popup is closed and Freebet remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - The selected free bet remains selected
        EXPECTED: - The odds boost button is rolled back to an unboosted state (show as BOOST)
        EXPECTED: - Odds of is rolled back to an unboosted state
        """
        pass

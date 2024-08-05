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
class Test_C12834352_Odds_Boost_functionality_in_Betslip(Common):
    """
    TR_ID: C12834352
    NAME: Odds Boost functionality in Betslip
    DESCRIPTION: This test case verifies Odds Boost functionality in Bet Slip
    DESCRIPTION: AUTOTEST MOBILE: [C57102581]
    DESCRIPTION: AUTOTEST DESKTOP: [C57119785]
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token with Any token value in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add OB token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Note: Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Load application and do NOT log in
    PRECONDITIONS: Fractional odds format selected for User1
    """
    keep_browser_open = True

    def test_001_add_a_single_selection_with_added_stake_to_the_betslipverify_that_odds_boost_button_is_not_shown_in_betslip(self):
        """
        DESCRIPTION: Add a single selection with added Stake to the Betslip
        DESCRIPTION: Verify that 'Odds boost' button is NOT shown in Betslip
        EXPECTED: 'BOOST' button is NOT shown in Betslip
        """
        pass

    def test_002_login_into_application_by_user_with_any_type_odds_boost_token_available(self):
        """
        DESCRIPTION: Login into Application by user with Any type Odds Boost token available
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed
        """
        pass

    def test_003_navigate_to_the_betslipverify_that_odds_boost_button_is_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to the Betslip
        DESCRIPTION: Verify that Odds Boost button is shown in Betslip
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOST' button is available
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon (with popup 'Hint Boost to increase the odds of the bets in your betslip! You can boost up to 50.00 total stake')
        EXPECTED: Est.returns/ Estimated returns(Coral), Pot. Returns / Potential returns(Ladbrokes)
        EXPECTED: ![](index.php?/attachments/get/33767)
        EXPECTED: ![](index.php?/attachments/get/33768)
        """
        pass

    def test_004_tap_boost_buttonverify_that_odds_are_boosted_and_odds_boost_button_is_displaying(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted and odds boost button is displaying
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        EXPECTED: ![](index.php?/attachments/get/33769)
        EXPECTED: ![](index.php?/attachments/get/33770)
        """
        pass

    def test_005_tap_boosted_buttonverify_that_odds_boost_button_is_shown_and_the_odds_boost_is_removed(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost button is shown and the odds boost is removed
        EXPECTED: - 'BOOSTED' button is changed back to 'BOOST' button
        EXPECTED: - Boosted odds are removed
        EXPECTED: - Est. returns/ Estimated returns(Coral), Pot. Returns / Potential returns(Ladbrokes) are updated back
        """
        pass

    def test_006_tap_boost_button_one_more_time_and_then_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button one more time and then tap 'Place Bet' button.
        DESCRIPTION: Verify that bet receipt is shown
        EXPECTED: Bet receipt is shown with the following elements:
        EXPECTED: - boost icon
        EXPECTED: - hardcoded text: "This bet has been boosted!"
        EXPECTED: - boost odds was taken by the user
        EXPECTED: - Est. returns/ Estimated returns(Coral), Pot. Returns / Potential returns(Ladbrokes appropriate to boosted odds
        """
        pass

    def test_007_provide_same_verifications_with_decimal_odds_format(self):
        """
        DESCRIPTION: Provide same verifications with decimal odds format
        EXPECTED: 
        """
        pass

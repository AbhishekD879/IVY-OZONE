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
class Test_C12834690_Price_changing_live_push_in_Bet_Slip_for_boosted_bet(Common):
    """
    TR_ID: C12834690
    NAME: Price changing (live push) in Bet Slip for boosted bet
    DESCRIPTION: This test case verifies price changing (live push) in Betslip for bet that is selected for an odds boost
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated (Fractional odds format selected for User)
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add selection to the Betslip
    PRECONDITIONS: Add Stake and tap 'Boost' button
    PRECONDITIONS: Change price for this bet in TI
    """
    keep_browser_open = True

    def test_001_verify_that_inline_message_is_displayed_at_the_topverify_message_content(self):
        """
        DESCRIPTION: Verify that inline message is displayed at the top
        DESCRIPTION: Verify message content
        EXPECTED: **Before OX99**
        EXPECTED: - Inline message is displayed at the top of Bet slip
        EXPECTED: - Text: 'Some of the prices have changed, please re-boost your bet!' (displayed until user takes an action such as re-boost or navigates away from page)'
        EXPECTED: **After OX99**
        EXPECTED: - No message at the top for Coral
        EXPECTED: - Only Ladbrokes: Message 'Some of the prices have changed, please Re-Boost your bet!' is shown for 5s
        EXPECTED: - Message 'Price changed from XX to XX' is shown above the selection
        EXPECTED: ![](index.php?/attachments/get/33751)
        EXPECTED: ![](index.php?/attachments/get/33750)
        """
        pass

    def test_002_verify_that_inline_message_is_displayed_at_the_bottomverify_message_content(self):
        """
        DESCRIPTION: Verify that inline message is displayed at the bottom
        DESCRIPTION: Verify message content
        EXPECTED: **Before OX99**
        EXPECTED: - Inline message is displayed at the bottom
        EXPECTED: - Text: 'Some of the prices have changed, please re-boost your bet!' (displayed until user takes an action such as re-boost or navigates away from page)
        EXPECTED: **After OX99**
        EXPECTED: - Notification message: 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted prices' is shown at the bottom of Betslip
        EXPECTED: ![](index.php?/attachments/get/33752)
        EXPECTED: ![](index.php?/attachments/get/33753)
        """
        pass

    def test_003_verify_that_boost_button_text_changes_to_re_boost(self):
        """
        DESCRIPTION: Verify that boost button text changes to 'RE-BOOST'
        EXPECTED: Boost button text changes to 'RE-BOOST'
        """
        pass

    def test_004_verify_that_the_non_boosted_striked_out_price_is_updated(self):
        """
        DESCRIPTION: Verify that the non-boosted striked out price is updated
        EXPECTED: The non-boosted striked out price is updated (according to the updated value in TI from preconditions)
        """
        pass

    def test_005_verify_that_boosted_price_remains_unchanged(self):
        """
        DESCRIPTION: Verify that boosted price remains unchanged
        EXPECTED: The boosted price remains unchanged
        """
        pass

    def test_006_verify_that_the_place_bet_button_is_changed_to_accept__place_bet(self):
        """
        DESCRIPTION: Verify that the 'PLACE BET' button is changed to 'ACCEPT & PLACE BET'
        EXPECTED: The 'Place bet' button displays: 'ACCEPT & PLACE BET'
        EXPECTED: **After OX99**
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        EXPECTED: Ladbrokes: ''ACCEPT AND PLACE BET'
        """
        pass

    def test_007_tap_re_boost_buttonverify_that_boosted_odds_are_updated(self):
        """
        DESCRIPTION: Tap 'RE-BOOST' button
        DESCRIPTION: Verify that boosted odds are updated
        EXPECTED: - Betslip is reloaded
        EXPECTED: - Boosted odds are updated
        """
        pass

    def test_008_verify_that_accept__place_bet_button_is_changed_back_to_place_bet(self):
        """
        DESCRIPTION: Verify that 'ACCEPT & PLACE BET' button is changed back to 'PLACE BET'
        EXPECTED: 'PLACE BET' button is shown
        """
        pass

    def test_009_tap_place_bet_buttonverify_that_the_bet_is_placed_at_the_boosted_odds(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        DESCRIPTION: Verify that the bet is placed at the boosted odds
        EXPECTED: The bet is placed at the boosted odds
        """
        pass

    def test_010_add_selection_to_the_betslip_one_more_timeadd_stake_and_tap_boost_button(self):
        """
        DESCRIPTION: Add selection to the Betslip one more time
        DESCRIPTION: Add stake and tap ''BOOST'' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED'
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        pass

    def test_011_change_price_for_this_selection_in_tirepeat_steps_1_6(self):
        """
        DESCRIPTION: Change price for this selection in TI
        DESCRIPTION: Repeat steps #1-6
        EXPECTED: Results are the same
        """
        pass

    def test_012_tap_accept__place_bet_button__verify_that_the_updated_boosted_prices_are_retrieved__verify_that_the_bet_is_placed_at_the_boosted_odds(self):
        """
        DESCRIPTION: Tap 'ACCEPT & PLACE BET' button
        DESCRIPTION: - Verify that the updated boosted prices are retrieved
        DESCRIPTION: - Verify that the bet is placed at the boosted odds
        EXPECTED: - Updated boosted prices are retrieved
        EXPECTED: - The bet is placed at the boosted odds
        """
        pass

    def test_013_provide_same_verifications_with_decimal_odds_format(self):
        """
        DESCRIPTION: Provide same verifications with decimal odds format
        EXPECTED: 
        """
        pass

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
class Test_C2987453_Verify_price_changing_live_push_in_Quick_Bet_for_boosted_bet(Common):
    """
    TR_ID: C2987453
    NAME: Verify price changing (live push) in Quick Bet for boosted bet
    DESCRIPTION: This test case verifies price changing (live push) in Quick Bet for boosted bet
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add selection to the Quickbet
    PRECONDITIONS: Add stake and tap 'Boost' button
    PRECONDITIONS: Change price for this bet in https://backoffice-tst2.coral.co.uk/ti
    """
    keep_browser_open = True

    def test_001_verify_that_inline_message_is_displayed_at_the_topverify_message_content(self):
        """
        DESCRIPTION: Verify that inline message is displayed at the top
        DESCRIPTION: Verify message content
        EXPECTED: Inline message is displayed at the top.
        EXPECTED: Text: 'Price changed from X/X to Y/Y'
        """
        pass

    def test_002_verify_that_inline_message_is_displayed_at_the_bottomverify_message_content(self):
        """
        DESCRIPTION: Verify that inline message is displayed at the bottom
        DESCRIPTION: Verify message content
        EXPECTED: Inline message is displayed at the bottom.
        EXPECTED: Text: 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted price' (displayed until user takes an action such as re-boost or navigates away from page)
        """
        pass

    def test_003_verify_that_boost_button_text_changes_to_re_boost(self):
        """
        DESCRIPTION: Verify that boost button text changes to 'RE-BOOST'
        EXPECTED: Boost button text changes to 'RE-BOOST'
        """
        pass

    def test_004_verify_that_the_boost_button_remains_selected(self):
        """
        DESCRIPTION: Verify that the boost button remains selected
        EXPECTED: The boost button remains selected
        """
        pass

    def test_005_verify_that_the_non_boosted_striked_out_price_is_updated(self):
        """
        DESCRIPTION: Verify that the non-boosted striked out price is updated
        EXPECTED: The non-boosted striked out price is updated (according to the value in https://backoffice-tst2.coral.co.uk/ti from preconditions)
        """
        pass

    def test_006_verify_that_boosted_price_remains_unchanged(self):
        """
        DESCRIPTION: Verify that boosted price remains unchanged
        EXPECTED: The boosted price remains unchanged
        """
        pass

    def test_007_verify_that_the_place_bet_button_displays_accept__place_bet(self):
        """
        DESCRIPTION: Verify that the 'Place bet' button displays: 'ACCEPT & PLACE BET'
        EXPECTED: The 'Place bet' button displays: 'ACCEPT & PLACE BET'
        """
        pass

    def test_008_tap_accept__place_bet_buttonverify_that_the_updated_boosted_prices_are_retrievedverify_that_the_bet_is_placed_at_the_boosted_odds(self):
        """
        DESCRIPTION: Tap 'ACCEPT & PLACE BET' button
        DESCRIPTION: Verify that the updated boosted prices are retrieved
        DESCRIPTION: Verify that the bet is placed at the boosted odds
        EXPECTED: - Updated boosted prices are retrieved
        EXPECTED: - The bet is placed at the boosted odds
        """
        pass

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
class Test_C15392888_Verify_bet_placement_during_price_change_in_case_liveserve_updates_do_not_work_on_Betslip(Common):
    """
    TR_ID: C15392888
    NAME: Verify bet placement during price change in case liveserve updates do not work on Betslip
    DESCRIPTION: This test case verified that user successfully place a bet in case price changing and liveserve is not working
    PRECONDITIONS: Ask the developer to build the env where liveserve is NOT working
    PRECONDITIONS: 1. Login with user who has at least 2 odds boost tokens (Use instruction to create and add odds boost for user: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token)
    """
    keep_browser_open = True

    def test_001_add_selection_to_betslipnavigate_to_betslip_and_add_stake_for_selectionin_same_time_change_price_for_appropriate_selection_in_tiverify_that_price_change_is_not_shown_in_betslip_because_liveserve_is_not_working(self):
        """
        DESCRIPTION: Add selection to Betslip
        DESCRIPTION: Navigate to Betslip and add Stake for selection
        DESCRIPTION: In same time change price for appropriate selection in TI
        DESCRIPTION: Verify that price change is not shown in Betslip because liveserve is not working
        EXPECTED: Price changing is not shown in Betslip
        """
        pass

    def test_002_tap_boost_buttonverify_that_the_odds_is_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that the odds is boosted
        EXPECTED: - 'BOOST' button changed to 'BOOSTED'
        EXPECTED: - Original and boosted odds are shown (original odds is not updated)
        """
        pass

    def test_003_tap_place_bet_buttonverify_that_bet_is_placed_with_updated_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with updated boosted odds
        EXPECTED: Bet receipt is shown with:
        EXPECTED: - Updated boosted odds
        EXPECTED: - 'This bet has been boosted' label
        """
        pass

    def test_004_tap_reuse_selection_button_and_add_stake_for_selectiontap_boost_buttonverify_that_boosted_odds_is_shown_boosted_odds_are_the_same_as_on_bet_receipt_in_step_3(self):
        """
        DESCRIPTION: Tap 'Reuse selection' button and add stake for selection
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that boosted odds is shown (boosted odds are the same as on bet receipt in step #3)
        EXPECTED: - 'BOOST' button changed to 'BOOSTED'
        EXPECTED: - Boosted odds is shown
        """
        pass

    def test_005_in_same_time_change_price_for_appropriate_selection_in_tiverify_that_price_change_is_not_shown_in_betslip_because_liveserve_is_not_working(self):
        """
        DESCRIPTION: In same time change price for appropriate selection in TI
        DESCRIPTION: Verify that price change is not shown in Betslip because liveserve is not working
        EXPECTED: Verify that price change is not shown
        """
        pass

    def test_006_tap_place_bet_buttonverify_that_price_change_messages_and_re_boost_button_are_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that price change messages and 'RE-BOOST' button are shown
        EXPECTED: - 'RE-BOOST' button is shown
        EXPECTED: - Price change messages are shown for:
        EXPECTED: Coral:
        EXPECTED: Messages: 'The price has changed and a new boosted odds will be applied to your bet. Hit Re-Boost to see you new boosted price' at the bottom of Betslip
        EXPECTED: Ladbrokes:
        EXPECTED: Message 'Some of prices have changed! Please re-boost your bet' is shown on the top of Betslip for 5s
        EXPECTED: Message: 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted prices' at the bottom of Betslip
        EXPECTED: - 'Price changed from XX to XX' is shown above the selection for Coral and Ladbrokes
        EXPECTED: -  'ACCEPT & Place BET' (Coral) 'ACCEPT AND PLACE BET' (Ladbrokes)  is shown
        """
        pass

    def test_007_tap_re_boost_buttonverify_that_odds_is_re_boosted_and_messages_dissapeared(self):
        """
        DESCRIPTION: Tap 'Re-BOOST' button
        DESCRIPTION: Verify that odds is re-boosted and messages dissapeared
        EXPECTED: - Messages for price change are NOT shown
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Updated original and boosted odds are shown
        """
        pass

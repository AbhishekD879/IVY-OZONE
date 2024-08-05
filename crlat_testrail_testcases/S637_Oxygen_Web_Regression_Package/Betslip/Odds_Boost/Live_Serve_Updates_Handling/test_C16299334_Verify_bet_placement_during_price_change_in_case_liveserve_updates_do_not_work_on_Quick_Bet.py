import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C16299334_Verify_bet_placement_during_price_change_in_case_liveserve_updates_do_not_work_on_Quick_Bet(Common):
    """
    TR_ID: C16299334
    NAME: Verify bet placement during price change in case liveserve updates do not work on Quick Bet
    DESCRIPTION: This test case verified that user successfully place a bet in case price changing and liveserve is not working
    PRECONDITIONS: Ask the developer to build the env where liveserve is NOT working
    PRECONDITIONS: Login with user who has at least 2 odds boost tokens (Use instruction to create and add odds boost for user: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token)
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betadd_stake_for_selectionin_same_time_change_price_for_appropriate_selection_in_tiverify_that_price_change_is_not_shown_in_quick_bet_because_liveserve_is_not_working(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        DESCRIPTION: Add Stake for selection
        DESCRIPTION: In same time change price for appropriate selection in TI
        DESCRIPTION: Verify that price change is not shown in Quick Bet because liveserve is not working
        EXPECTED: Price changing is not shown in Quick Bet
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

    def test_003_tap_place_bet_buttonverify_that_message_for_price_change_and_re_boost_button_are_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that message for price change and RE-BOOST button are shown
        EXPECTED: - 'RE-BOOST' button is shown
        EXPECTED: - 'Price changed from XX to XX' message is shown above the selection
        EXPECTED: - 'The price has changed and a new boosted odds will be applied to your bet. Hit Re-Boost to see you new boosted price' is shown at the bottom of Quick Bet
        """
        pass

    def test_004_tap_accept__place_bet_coral__accept_and_place_bet_ladbrokesverify_that_bet_is_place_successfully(self):
        """
        DESCRIPTION: Tap 'ACCEPT & Place BET' (Coral) / 'ACCEPT AND PLACE BET' (Ladbrokes)
        DESCRIPTION: Verify that bet is place successfully
        EXPECTED: - Bet is placed with boosted odds
        """
        pass

    def test_005_add_selection_one_more_time_to_quick_bettap_boost_buttonverify_that_odds_is_boosted(self):
        """
        DESCRIPTION: Add selection one more time To Quick Bet
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds is boosted
        EXPECTED: - 'BOOST' button changed to 'BOOSTED'
        EXPECTED: - Original and boosted odds are shown (original odds is not updated)
        """
        pass

    def test_006_in_same_time_change_price_for_appropriate_selection_in_tiverify_that_price_change_is_not_shown_in_quick_bet_because_liveserve_is_not_working(self):
        """
        DESCRIPTION: In same time change price for appropriate selection in TI
        DESCRIPTION: Verify that price change is not shown in Quick Bet because liveserve is not working
        EXPECTED: Price changing is not shown in Quick Bet
        """
        pass

    def test_007_tap_place_bet_buttonverify_that_message_for_price_change_and_re_boost_button_are_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that message for price change and RE-BOOST button are shown
        EXPECTED: - 'RE-BOOST' button is shown
        EXPECTED: - 'Price changed from XX to XX' message is shown above the selection
        EXPECTED: - 'The price has changed and a new boosted odds will be applied to your bet. Hit Re-Boost to see you new boosted price' is shown at the bottom of Quick Bet
        """
        pass

    def test_008_tap_accept__place_bet_coral__accept_and_place_bet_ladbrokesverify_that_bet_is_place_successfully(self):
        """
        DESCRIPTION: Tap 'ACCEPT & Place BET' (Coral) / 'ACCEPT AND PLACE BET' (Ladbrokes)
        DESCRIPTION: Verify that bet is place successfully
        EXPECTED: - Bet is placed with boosted odds
        """
        pass

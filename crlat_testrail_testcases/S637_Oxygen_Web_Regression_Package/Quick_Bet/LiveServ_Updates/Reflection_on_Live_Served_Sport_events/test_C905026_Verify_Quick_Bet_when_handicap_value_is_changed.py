import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C905026_Verify_Quick_Bet_when_handicap_value_is_changed(Common):
    """
    TR_ID: C905026
    NAME: Verify Quick Bet when handicap value is changed
    DESCRIPTION: This case verifies Quick Bet when handicap value is changed
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * To check handicap value correctness open Dev Tools -> Networks -> WS -> '?EIO=3&transport=websocket' request -> Frames section
    PRECONDITIONS: * Load app
    PRECONDITIONS: * Go to In Play Sport EDP where handicap markers are present
    PRECONDITIONS: * OpenBet TI tool https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_add_selection_that_contains_handicap_value_to_quick_bet(self):
        """
        DESCRIPTION: Add selection that contains Handicap value to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventchange_rawhandicapvalue_on_market_level_in_ob_ti_tooland_at_the_same_time_have_quick_bet_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change **rawHandicapValue** on market level in OB TI tool
        DESCRIPTION: and at the same time have Quick Bet page opened to watch for updates
        EXPECTED: Handicap value in selection name is updated
        """
        pass

    def test_003_verify_error_message_and_login__place_betplace_bet_button(self):
        """
        DESCRIPTION: Verify Error message and 'LOGIN & PLACE BET'/'PLACE BET' button
        EXPECTED: * 'Line Change from #OLD to #NEW' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: * 'LOGIN & PLACE BET'/'ACCEPT & PLACE BET' button remains disabled(not clickable)
        """
        pass

    def test_004_verify_new_handicap_value_on_ws(self):
        """
        DESCRIPTION: Verify NEW handicap value on WS
        EXPECTED: NEW handicap value corresponds to one that is received in response from TI - MSEVENT0000#### push request with 'raw_hcap' value and WS - 'remotebetslip' - 'sEVMKT###...' - 'message: raw_hcap'
        """
        pass

    def test_005_change_price_for_respective_handicap_market_and_make_no_changes_on_market_handicap_value(self):
        """
        DESCRIPTION: Change price for respective handicap market and make no changes on market handicap value
        EXPECTED: Price value is changed and handicap value remains the same
        """
        pass

    def test_006_enter_value_in_stake_field_for_bet_and_tapclick_login__place_betaccept__place_bet_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for bet and tap/click 'LOGIN & PLACE BET'/'ACCEPT & PLACE BET' button
        EXPECTED: Login pop-up window should be displayed OR Bet is placed
        """
        pass

    def test_007_repeat_steps_2_6_for_a_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps #2-6 for a logged in user
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_6_for_different_kind_of_sports(self):
        """
        DESCRIPTION: Repeat steps #2-6 for different kind of sports
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_2_6_for_not_in_play_sports(self):
        """
        DESCRIPTION: Repeat steps #2-6 for not In-Play Sports
        EXPECTED: 
        """
        pass

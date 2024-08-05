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
class Test_C863011_Needs_to_be_updatedVerify_error_handling_during_bet_placement(Common):
    """
    TR_ID: C863011
    NAME: [Needs to be updated]Verify error handling during bet placement
    DESCRIPTION: This test case verifies handling during bet placement within Quick Bet
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Help from developer side is needed in order to run this test case
    PRECONDITIONS: * User should have free bets added to his account
    PRECONDITIONS: * [How to add Free bets to user`s account] [1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * Free Bets drop-down is displayed above Quick Stakes buttons
        """
        pass

    def test_003_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: * 'Stake' field is populated with entered value
        """
        pass

    def test_004__tap_place_bet_button_trigger_situation_when_incorrectunparsable_price_is_sent_to_place_a_bet(self):
        """
        DESCRIPTION: * Tap 'PLACE BET' button
        DESCRIPTION: * Trigger situation when incorrect/unparsable price is sent to place a bet
        EXPECTED: The next error is received in 31012 response in WS:
        EXPECTED: {"data":{"error":{"code":"INTERNAL_INVALID_REQUEST","description":"Error parsing price For input string: \"value where error appears\""}}}
        """
        pass

    def test_005_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: * Bet is NOT placed
        EXPECTED: * Warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        """
        pass

    def test_006_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_007__tap_place_bet_button_trigger_situation_when_bpp_returns_internal_error(self):
        """
        DESCRIPTION: * Tap 'PLACE BET' button
        DESCRIPTION: * Trigger situation when BPP returns internal error
        EXPECTED: The next error is received in 31012 response in WS:
        EXPECTED: {"data":{"error":{"code":"SERVICE_ERROR","description":"Unknown error: clz\u003djava.lang.NullPointerException,msg\u003dnull,coz\u003dnull"}}}
        """
        pass

    def test_008_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_009__tap_place_bet_button_trigger_situation_when_error_returned_from_ob_in_case_when_user_places_a_bet_with_outdated_price(self):
        """
        DESCRIPTION: * Tap 'PLACE BET' button
        DESCRIPTION: * Trigger situation when error returned from OB in case when user places a bet with outdated price
        EXPECTED: The next error is received in 31012 response in WS:
        EXPECTED: {"data":{"error":{"code":"VALIDATION_ERROR"}}}
        """
        pass

    def test_010_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_011_choose_free_bet_from_free_bets_drop_down_and_repeat_steps_4_10(self):
        """
        DESCRIPTION: Choose Free bet from Free bets drop-down and repeat steps #4-10
        EXPECTED: 
        """
        pass

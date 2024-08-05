import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C883636_Verify_Bet_Placement_when_Stake_is_bigger_than_Max_Stake(Common):
    """
    TR_ID: C883636
    NAME: Verify Bet Placement when Stake is bigger than Max Stake
    DESCRIPTION: This test case verifies Bet Placement within Quick Bet when Stake is bigger than Max Stake
    DESCRIPTION: AUTOTEST: [C1293645]
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in, has positive balance and free bets added
    PRECONDITIONS: * 'MaxStake' value can be viewed or changed on selection level in OpenBet Ti tool
    PRECONDITIONS: * To disable Overask for the Customer/Event type please follow this path: Backoffice Tool -> Trader Interface -> Customer -> (Search by Username) -> Click on the Account name -> Account Rules -> Select No Intercept value in the Control column -> click Update
    PRECONDITIONS: * Open Dev Tools -> Network -> WS -> Frames to see response
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_one_sport_selection(self):
        """
        DESCRIPTION: Tap one <Sport> selection
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_003_enter_value_which_is_bigger_than_maxstake_allowed_in_stake_field(self):
        """
        DESCRIPTION: Enter value which is bigger than **maxStake** allowed in 'Stake' field
        EXPECTED: * 'Stake' field is populated with entered value
        """
        pass

    def test_004_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Sorry, the maximum stake for the bet is <currency> <amount>' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: ,
        EXPECTED: where <currency> is the same as during registration
        """
        pass

    def test_005_verify_amount_value_displayed_on_error_message(self):
        """
        DESCRIPTION: Verify 'amount' value displayed on error message
        EXPECTED: 'amount' value corresponds to **data.error.stake.maxAllowed** attribute from 31012 response from WS
        """
        pass

    def test_006_verify_warning_message_presence(self):
        """
        DESCRIPTION: Verify warning message presence
        EXPECTED: Warning message does not disappear after tapping out of its area
        """
        pass

    def test_007_remove_value_from_stake_field_and_select_free_bet_from_pop_up_with_the_same_amount_that_is_equal_to_maxallowed__value_returned_from_response(self):
        """
        DESCRIPTION: Remove value from 'Stake' field and select free bet from pop up with the same amount that is equal to **'maxAllowed'**  value returned from response
        EXPECTED: * 'Stake' field is empty
        EXPECTED: * Free bet is chosen
        """
        pass

    def test_008_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_009_repeat_steps_6_8_but_on_step_6_enter_stake_and_choose_free_bet_in_that_way_that_their_sum_is_equal_or_less_than_maxallowed__value_returned_from_the_response(self):
        """
        DESCRIPTION: Repeat steps #6-8 but on step 6 enter stake and choose free bet in that way that their sum is equal or less than **'maxAllowed'**  value returned from the response
        EXPECTED: 
        """
        pass

    def test_010_tap_x_button_on_quick_bet(self):
        """
        DESCRIPTION: Tap 'X' button on Quick Bet
        EXPECTED: Quick Bet is closed
        """
        pass

    def test_011_add__lp_race_selection_to_quick_bet_and_repeat_steps_3_10(self):
        """
        DESCRIPTION: Add  LP <Race> selection to Quick Bet and repeat steps #3-10
        EXPECTED: 
        """
        pass

    def test_012_add__sp_race_selection_to_quick_bet_and_repeat_steps_3_10(self):
        """
        DESCRIPTION: Add  SP <Race> selection to Quick Bet and repeat steps #3-10
        EXPECTED: 
        """
        pass

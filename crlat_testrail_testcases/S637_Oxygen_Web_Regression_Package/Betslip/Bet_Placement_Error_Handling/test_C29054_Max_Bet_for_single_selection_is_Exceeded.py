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
class Test_C29054_Max_Bet_for_single_selection_is_Exceeded(Common):
    """
    TR_ID: C29054
    NAME: Max Bet for single selection is Exceeded
    DESCRIPTION: This test case verifies bet slip error handling in case when user's individual Max bet for selected market is exceeded
    DESCRIPTION: **JIRA tickets:**
    DESCRIPTION: BMA-21529: New betslip - Max bet alert
    DESCRIPTION: AUTOTEST: [C869055]
    DESCRIPTION: AUTOTEST [C1502044]
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  The user's account balance is sufficient to cover the max bet stake
    PRECONDITIONS: 3. Overask is turned off for used user
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event landing page
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_002_enter_stake_value_which_exceeds_max_bet_stake_for_current_event_in_stake_fieldclick_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: Enter stake value which exceeds Max Bet Stake for current event in 'Stake' field
        DESCRIPTION: Click 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: [Not actual from OX 99]
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Sorry, the maximum stake for the bet is <currency> <amount>' error message is displayed
        EXPECTED: where <currency> is the same as during registration
        EXPECTED: [From OX 99]
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Maximum stake is <currency><amount>' error message is displayed above stake section
        EXPECTED: * Place Bet button is active
        """
        pass

    def test_003_remove_value_from_stake_field_and_select_free_bet_from_drop_down_with_the_same_amount_that_is_equal_to_maxallowed_value_returned_from_placebet_response(self):
        """
        DESCRIPTION: Remove value from 'Stake' field and select free bet from drop-down with the same amount that is equal to 'maxAllowed' value returned from 'placeBet' response
        EXPECTED: * 'Stake' field is empty
        EXPECTED: * Free bet is chosen
        """
        pass

    def test_004_tap_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_005_repeat_steps_3_4_but_choose_free_bet_in_that_way_that_amount_is_more_than_maxallowed_value_returned_from_placebet_response(self):
        """
        DESCRIPTION: Repeat steps #3-4 but choose free bet in that way that amount is more than 'maxAllowed' value returned from 'placeBet' response
        EXPECTED: [Not actual from OX 99]
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Sorry, the maximum stake for the bet is <currency> <amount>' error message is displayed
        EXPECTED: where <currency> is the same as during registration
        EXPECTED: [From OX 99]
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Maximum stake is <currency><amount>' error message is displayed above stake section
        EXPECTED: * Place Bet button is active
        """
        pass

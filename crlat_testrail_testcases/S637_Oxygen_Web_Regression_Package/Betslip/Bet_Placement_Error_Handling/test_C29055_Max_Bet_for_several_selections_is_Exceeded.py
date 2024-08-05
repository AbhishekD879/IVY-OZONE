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
class Test_C29055_Max_Bet_for_several_selections_is_Exceeded(Common):
    """
    TR_ID: C29055
    NAME: Max Bet for several selections is Exceeded
    DESCRIPTION: This test case verifies Error Handling When Max Bet for several selections is Exceeded
    DESCRIPTION: **JIRA tickets:**
    DESCRIPTION: BMA-21529: New betslip - Max bet alert
    DESCRIPTION: AUTOTEST: [C871649]
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. The user's account balance is sufficient to cover the max bet stake
    PRECONDITIONS: 3. Overask is turned off for used user
    PRECONDITIONS: 4. App is loaded
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races>  it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event landing page
    """
    keep_browser_open = True

    def test_001_add_few_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add few selections to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_002_enter_stake_value_which_exceeds_max_bet_stake_for_particular_event_in_stake_fieldclick_place_bet_button(self):
        """
        DESCRIPTION: Enter stake value which exceeds Max Bet Stake for particular event in 'Stake' field
        DESCRIPTION: Click 'Place Bet' button
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: * Place Bet button is active
        """
        pass

    def test_003_enter_correct_stakes_which_is_equivalent_to_max_bet_and_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Enter correct stakes which is equivalent to max bet and tap on 'Place Bet' button
        EXPECTED: * Bet is placed
        EXPECTED: * User balance is decreased by value entered in stake field
        """
        pass

    def test_004_remove_value_from_stake_field_and_select_free_bet_from_drop_down_with_the_same_amount_that_is_equal_to_maxallowed_value_returned_from_placebet_response_and_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Remove value from 'Stake' field and select free bet from drop-down with the same amount that is equal to 'maxAllowed' value returned from 'placeBet' response and tap on 'Place Bet' button
        EXPECTED: * Bet is placed
        EXPECTED: * User balance is decreased by value entered in stake field
        """
        pass

    def test_005_enter_a_stakes_but_make_sure_max_bets_are_changed_via_liveserv___tap_on_place_bet_button(self):
        """
        DESCRIPTION: Enter a stakes but make sure Max Bets are changed via LiveServ -> tap on 'Place Bet' button
        EXPECTED: Max Bet amount can be changed.
        EXPECTED: 1.  In case if entered stakes are still higher then 'max bet' -> results will be the same as in steps #3
        EXPECTED: 2.  In case if entered stakes are less then 'max bet' -> bets will be placed
        """
        pass

    def test_006_add_two_or_more_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more selections from different events to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_007_open_bet_slip_multiples_section(self):
        """
        DESCRIPTION: Open Bet Slip, 'Multiples' section
        EXPECTED: 'Multiples' section is opened
        """
        pass

    def test_008_repeat_steps__3___6(self):
        """
        DESCRIPTION: Repeat steps # 3 - 6
        EXPECTED: 
        """
        pass

import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870401_18Customer_Bet_placements_fails_on_an_in_play_event_where_betting_is_not_allowed_once_event_starts_and_event_suspended_error_message_displays(Common):
    """
    TR_ID: C44870401
    NAME: 18.Customer Bet placements fails on an in play event where betting is not allowed once event starts and event suspended error message displays
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_a_selection_from_a_banache_market_just_before_the_event_starts(self):
        """
        DESCRIPTION: Add a selection from a Banache market just before the event starts
        EXPECTED: You should have added a selection from a Banache market just before the event starts
        """
        pass

    def test_002_try_and_place_a_bet_on_the_selection_when_it_starts(self):
        """
        DESCRIPTION: Try and place a bet on the selection when it starts
        EXPECTED: You should not be able to place the bet and you should see a suspended message in the bet slip
        """
        pass

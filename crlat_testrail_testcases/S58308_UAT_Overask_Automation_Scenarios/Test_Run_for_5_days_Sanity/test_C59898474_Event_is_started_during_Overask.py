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
class Test_C59898474_Event_is_started_during_Overask(Common):
    """
    TR_ID: C59898474
    NAME: Event is started during Overask
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_select_hr_event_which_is_about_to_start_and_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Select HR event which is about to start and add selection to Quick Bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_event_is_started_during_overask(self):
        """
        DESCRIPTION: Event is started during overask
        EXPECTED: Suspension message is shown in betslip
        EXPECTED: The counter should be shown with messaging("Your bet has not been accepted by trader") - if error message received during the Oxi call, if not then should continue with normal bet placement flow and will receive error when attempting to place the bet.
        """
        pass

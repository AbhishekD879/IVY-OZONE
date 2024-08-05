import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870211_Preplay_Racing_Bet_placement_(Common):
    """
    TR_ID: C44870211
    NAME: Preplay Racing Bet placement "
    DESCRIPTION: "Customer places a single , Forecast and Tricast bet on HR and GH race
    DESCRIPTION: Verify display of forecast/tricast in the betslip
    DESCRIPTION: - selection name
    DESCRIPTION: - 1st/2nd/3rd where appropriate
    DESCRIPTION: - event name"
    PRECONDITIONS: UserName: goldenbuild1 Password: password1
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: HomePage is displayed
        """
        pass

    def test_002_go_to_hrgh_racing(self):
        """
        DESCRIPTION: Go to HR/GH racing
        EXPECTED: Racing landing page opened
        """
        pass

    def test_003_click_on_any_event_meeting(self):
        """
        DESCRIPTION: Click on any event meeting
        EXPECTED: Race card page opened
        """
        pass

    def test_004_make_a_selection_from_win_each_way_market(self):
        """
        DESCRIPTION: Make a selection from Win each way market
        EXPECTED: Selection added to betsip
        """
        pass

    def test_005_verify_selection_details_in_betslip(self):
        """
        DESCRIPTION: Verify selection details in betslip
        EXPECTED: Event Name
        EXPECTED: Market Name
        EXPECTED: Meeting time
        EXPECTED: Odds
        EXPECTED: Stake box
        EXPECTED: Potential returns
        EXPECTED: EW box
        EXPECTED: Total stake
        EXPECTED: Total potential returns
        """
        pass

    def test_006_verify_tapping_on_place_bet_bet_is_placed(self):
        """
        DESCRIPTION: Verify tapping on 'Place bet' bet is placed
        EXPECTED: Bet is placed
        EXPECTED: Betslip appear with details
        EXPECTED: Single@x/x
        EXPECTED: Receipt No:
        EXPECTED: Meeting name
        EXPECTED: Market name / Meeting time & name
        EXPECTED: Cashout - if applicable
        EXPECTED: Stake for this bet
        EXPECTED: Potential returns
        EXPECTED: Total stake
        EXPECTED: Total potential returns
        EXPECTED: Resure selection & G Betting tab
        """
        pass

    def test_007_repeat_steps_4_to_8_for_forecast_and_tricast_bets(self):
        """
        DESCRIPTION: Repeat steps #4 to #8 for forecast and tricast bets
        EXPECTED: 
        """
        pass

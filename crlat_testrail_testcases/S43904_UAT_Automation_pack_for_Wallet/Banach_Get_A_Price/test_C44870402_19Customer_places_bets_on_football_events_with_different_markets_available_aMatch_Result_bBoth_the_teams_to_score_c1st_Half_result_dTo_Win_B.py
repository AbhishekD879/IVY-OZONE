import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870402_19Customer_places_bets_on_football_events_with_different_markets_available_aMatch_Result_bBoth_the_teams_to_score_c1st_Half_result_dTo_Win_Both_the_teams_to_score_eHalf_time_Full_time_ETC(Common):
    """
    TR_ID: C44870402
    NAME: "19.Customer places bets on football events with different markets available a)Match Result b)Both the teams to score c)1st Half result d)To Win & Both the teams to score e)Half time /Full time ETC"
    DESCRIPTION: "19.Customer places bets on football events with different markets available
    DESCRIPTION: a)Match Result
    DESCRIPTION: b)Both the teams to score
    DESCRIPTION: c)1st Half result
    DESCRIPTION: d)To Win & Both the teams to score
    DESCRIPTION: e)Half time /Full time ETC"
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_bets_on_football_events_with_different_markets_available_egamatch_resultbboth_the_teams_to_scorec1st_half_resultdto_win__both_the_teams_to_scoreehalf_time_full_time_etc(self):
        """
        DESCRIPTION: Place bets on football events with different markets available e.g.
        DESCRIPTION: a)Match Result
        DESCRIPTION: b)Both the teams to score
        DESCRIPTION: c)1st Half result
        DESCRIPTION: d)To Win & Both the teams to score
        DESCRIPTION: e)Half time /Full time ETC"
        EXPECTED: You should have placed bets on different markets
        """
        pass

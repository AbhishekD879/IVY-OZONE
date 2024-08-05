import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - This script is limited to QA2 only as we are unable to retrieve multiple markets from single event in prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870402_19Customer_places_bets_on_football_events_with_different_markets_available_aMatch_Result_bBoth_the_teams_to_score_c1st_Half_result_dTo_Win_Both_the_teams_to_score_eHalf_time_Full_time_ETC(BaseBetSlipTest):
    """
    TR_ID: C44870402
    NAME: "19.Customer places bets on football events with different markets available a)Match Result b)Both the teams to score c)1st Half result d)To Win & Both the teams to score e)Half time /Full time ETC"
    DESCRIPTION: "19.Customer places bets on football events with different markets available
    DESCRIPTION: a)Match Result
    DESCRIPTION: b)Both the teams to score
    DESCRIPTION: c)1st Half result
    DESCRIPTION: d)To Win & Both the teams to score
    DESCRIPTION: e)Half time /Full time ETC"
    """
    keep_browser_open = True
    event_markets = [
        ('both_teams_to_score', {'cashout': True}),
        ('over_under_total_goals', {'cashout': True}),
        ('to_win_not_to_nil', {'cashout': True}),
        ('first_half_result', {'cashout': True}),
        ('score_goal_in_both_halves', {'cashout': True})]

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
        event_params = self.ob_config.add_autotest_premier_league_football_event(
            markets=self.event_markets)
        selection_ids = event_params.selection_ids
        # TODO
        # When match result market is added ,while placing bet the error "Server is unavialable at the moment.please try again later" is appearing
        # The match result market is not added.
        selection_id_2 = list(selection_ids['both_teams_to_score'].values())[0]
        selection_id_3 = list(selection_ids['over_under_total_goals'].values())[0]
        selection_id_4 = list(selection_ids['to_win_not_to_nil'].values())[1]
        selection_id_5 = list(selection_ids['first_half_result'].values())[0]
        selection_id_6 = list(selection_ids['score_goal_in_both_halves'].values())[1]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=(selection_id_2, selection_id_3, selection_id_4,
                                                         selection_id_5, selection_id_6))
        bet_info = self.place_and_validate_single_bet(number_of_stakes=6)
        self.check_bet_receipt_is_displayed()
        self.check_bet_receipt(betslip_info=bet_info)

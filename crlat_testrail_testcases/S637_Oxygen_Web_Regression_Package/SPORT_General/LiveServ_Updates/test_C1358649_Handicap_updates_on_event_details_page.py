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
class Test_C1358649_Handicap_updates_on_event_details_page(Common):
    """
    TR_ID: C1358649
    NAME: Handicap updates on event details page
    DESCRIPTION: This test case verifies live serve updates for handicap values on selections on event details page
    PRECONDITIONS: **Updates are received via push notifications**
    PRECONDITIONS: **Acceptance criteria**
    PRECONDITIONS: - Handicap updates should be tested both on In Play and Pre-match events.
    PRECONDITIONS: - Minimal scope of sports and index markets to test:
    PRECONDITIONS: <Basketball, American football, Ice hockey, Baseball>: Spread and total points markets.
    PRECONDITIONS: Rugby: Handicap and Total match points markets.
    PRECONDITIONS: Cricket: Total runs player (or Team runs or Player runs) market
    PRECONDITIONS: **Set up**
    PRECONDITIONS: <Sport> Event should be LiveServed and should have an index market (the type of market having "Handicap" or "Higher/lower" value set in TI) assigned
    PRECONDITIONS: In order to have event on In Play page:
    PRECONDITIONS: 1. Event should be Live (isStarted=true)
    PRECONDITIONS: 2. Event should be in-Play:
    PRECONDITIONS: drilldown TagNames=EVFLAG_BL (in TI check "Bet In Play list")
    PRECONDITIONS: 3. Event should also have a primary market defined to be shown on In Play tab (check in devlog): <Basketball, American football, Ice hockey, Baseball> - Money line market, <Rugby, Cricket> - Match Betting market
    PRECONDITIONS: 4. isMarketBetInRun=true (In TI check Bet In Running)
    PRECONDITIONS: 5. rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"
    PRECONDITIONS: 6. Event, Market, Outcome should be Active ( eventStatusCode="A", marketStatusCode="A", outcomeStatusCode="A" )
    PRECONDITIONS: Note: not supported on football sport
    PRECONDITIONS: Handicap values updates are coming through push in the **hcap_values** object having various number of parameters depending on the index market:
    PRECONDITIONS: - Examples of Handicap markets that have 2 parameters (H , A that stand for Home and Away): Handicap 2-way, 1st quarter handicap with tie, 4th quarter spread, 3rd quarter spread alternative;
    PRECONDITIONS: - Example of Handicap market that has 3 parameters (H, A, L): Handicap 3-way
    PRECONDITIONS: - Examples of Total Points markets that have 4 parameters: (B, E, H, L): Total points, 4th quarter total points, totals over/under, Total runs player, Player runs, Team runs(main), Player fours
    PRECONDITIONS: *Handicap market  "Handicap 2-way" is called Spread in the app
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_the_in_play_ltbasketball_american_football_ice_hockey_baseballgt_event_having_setup_described_in_pre_conditions(self):
        """
        DESCRIPTION: Open event details page of the In Play &lt;Basketball, American football, Ice hockey, Baseball&gt; event having setup described in pre-conditions
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_trigger_the_following_situation_for_this_event_in_ti_for_the_handicap_market_with_2_parameters_exhandicap_2_way__to_change_rawhandicapvalue_add_change_a_value_to_the_filed_handicap_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Handicap market with 2 parameters (ex.Handicap 2-way ) to change **rawHandicapValue* :
        DESCRIPTION: Add (change) a value to the filed "Handicap" and save market
        EXPECTED: Handicap value is changed on the selections under the Handicap market without app refresh
        """
        pass

    def test_003_trigger_the_following_situation_for_this_event_in_ti_for_the_handicap_market_with_3_parameters_handicap_3_way__to_change_rawhandicapvalue_add_change_a_value_to_the_filed_handicap_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Handicap market with 3 parameters (Handicap 3-way ) to change **rawHandicapValue* :
        DESCRIPTION: Add (change) a value to the filed "Handicap" and save market
        EXPECTED: Handicap value is changed on the selections under the Handicap market without app refresh
        """
        pass

    def test_004_trigger_the_following_situation_for_this_event_in_ti_for_the_total_points_market_to_change_rawhandicapvalue_add_change_a_value_to_the_filed_higherlower_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Total Points market to change **rawHandicapValue* :
        DESCRIPTION: Add (change) a value to the filed "Higher/lower" and save market
        EXPECTED: Handicap value is changed on the selections under the Total Points market without app refresh
        """
        pass

    def test_005_open_event_details_page_of_the_in_play_rugby_event_having_setup_described_in_pre_conditions(self):
        """
        DESCRIPTION: Open event details page of the In Play Rugby event having setup described in pre-conditions
        EXPECTED: Event details page is opened
        """
        pass

    def test_006_trigger_the_following_situation_for_this_event_in_ti_for_the_handicap_market_to_change_rawhandicapvalue_add_change_a_value_to_the_filed_handicap_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Handicap market to change **rawHandicapValue* :
        DESCRIPTION: Add (change) a value to the filed "Handicap" and save market
        EXPECTED: Handicap value is changed on the selections under the Handicap market without app refresh
        """
        pass

    def test_007_trigger_the_following_situation_for_this_event_in_ti_for_the_total_match_points_market_to_change_rawhandicapvalueadd_change_a_value_to_the_filed_higherlower_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Total Match Points market to change **rawHandicapValue*:
        DESCRIPTION: Add (change) a value to the filed "Higher/lower" and save market
        EXPECTED: Handicap value is changed on the selections under the Total Match Points market without app refresh
        """
        pass

    def test_008_open_event_details_page_of_the_in_play_cricket_event_having_setup_described_in_pre_conditions(self):
        """
        DESCRIPTION: Open event details page of the In Play Cricket event having setup described in pre-conditions
        EXPECTED: Event details page is opened
        """
        pass

    def test_009_trigger_the_following_situation_for_this_event_in_ti_for_the_total_runs_player_or_team_runs_or_player_runs_market_to_change_rawhandicapvalueadd_change_a_value_to_the_filed_higherlower_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Total runs player (or Team runs or Player runs) market to change **rawHandicapValue*:
        DESCRIPTION: Add (change) a value to the filed "Higher/lower" and save market
        EXPECTED: Handicap value is changed on the selections under the Total runs player (or Team runs or Player runs) market without app refresh
        """
        pass

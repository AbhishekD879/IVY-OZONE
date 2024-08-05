import re
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.handicap
@pytest.mark.desktop
@pytest.mark.event_details
@vtest
class Test_C1358649_Handicap_updates_on_event_details_page(BaseCashOutTest):
    """
    TR_ID: C1358649
    NAME: Handicap updates on event details page
    DESCRIPTION: This test case verifies live serve updates for handicap values on selections on event details page
    """
    keep_browser_open = True
    handicap_updated_market = None
    new_handicap_value = '+22.0'
    basketball_event_markets = [
        ('total_points',),
        ('handicap_2_way',),
        ('handicap_3_way',)]
    rugby_event_markets = [
        ('handicap_2_way', ),
        ('total_match_points', )]
    cricket_event_markets = [
        ('total_sixes',),
        ('team_runs',)]

    def verify_handicap_updates_on_edp(self):
        outcome_groups = self.handicap_updated_market.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')
        for outcome_group_name, outcome_group in list(outcome_groups.items()):
            self.outcomes = outcome_group
            outcome_group_name_1 = re.findall('[+-]?\d*\.?\d+', outcome_group_name)
            outcome_group_name_2 = (outcome_group_name_1[0])
            handicap_sigh = outcome_group_name_2[:1]
            if handicap_sigh == '+':
                self.assertEqual(outcome_group_name_2, self.new_handicap_value,
                                 msg=f'Actual handicap value is "{outcome_group_name_2}"'
                                     f'is not match with expected handicap value "{self.new_handicap_value}"')
            else:
                self.assertEqual(outcome_group_name_2, "-22.0",
                                 msg=f'Actual handicap value is "{outcome_group_name_2}"'
                                     f'is not match with expected handicap value "{"-22.0"}"')

    def test_000_preconditions(self):
        """
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
        # Basketball event creation
        self.__class__.basketball_event_id = \
            self.ob_config.add_basketball_event_to_us_league(markets=self.basketball_event_markets, is_live=True).event_id
        self.__class__.bb_hc_2_way_market_id = self.ob_config.market_ids[self.basketball_event_id]['handicap_2_way']
        self.__class__.bb_total_points_market_id = self.ob_config.market_ids[self.basketball_event_id]['total_points']

        # Rugby event creation
        self.__class__.rugby_event_id = \
            self.ob_config.add_rugby_league_event_to_rugby_league_all_rugby_league(markets=self.rugby_event_markets, is_live=True).event_id

        self.__class__.rugby_hc_2_way_market_id = self.ob_config.market_ids[self.rugby_event_id]['handicap_2_way']
        self.__class__.rugby_tmp_market_id = self.ob_config.market_ids[self.rugby_event_id]['total_match_points']

        # Cricket event creation
        self.__class__.cricket_event_id = \
            self.ob_config.add_autotest_cricket_event(markets=self.cricket_event_markets, is_live=True).event_id
        self.__class__.cricket_hc_2_way_market_id = self.ob_config.market_ids[self.cricket_event_id]['team_runs']

    def test_001_open_event_details_page_of_the_in_play_basketball_american_football_ice_hockey_baseball_event_having_setup_described_in_pre_conditions(self):
        """
        DESCRIPTION: Open event details page of the In Play <Basketball, American football, Ice hockey, Baseball> event having setup described in pre-conditions
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.basketball_event_id)
        self.site.wait_content_state(state_name='EventDetails', timeout=20)
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.siteserve.EXPECTED_MARKET_TABS.all_markets,
                         msg=f'\nCurrent tab: "{current_tab}" '
                             f'is not as expected: "{vec.siteserve.EXPECTED_MARKET_TABS.all_markets}')
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        if self.brand == 'ladbrokes':
            self.__class__.handicap_two_way = 'Handicap 2-way'
            self.__class__.handicap_three_way = 'Handicap 3-way'
        else:
            self.__class__.handicap_two_way = 'Spread' if self.device_type == 'desktop' else 'SPREAD'
            self.__class__.handicap_three_way = 'Handicap 3-Way' if self.device_type == 'desktop' else 'HANDICAP 3-WAY'
        for market_name, market in list(markets_list.items()):
            if market_name == self.handicap_two_way:
                self.handicap_updated_market = market
                break
        self.assertTrue(self.handicap_updated_market, msg=f'*** Can not find "Handicap 2-way/Spread" market section')
        outcome_groups = self.handicap_updated_market.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg=f'Outcome groups is empty')

    def test_002_trigger_the_following_situation_for_this_event_in_ti_for_the_handicap_market_with_2_parameters_exhandicap_2_way__to_change_rawhandicapvalue_add_change_a_value_to_the_filed_handicap_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Handicap market with 2 parameters (ex.Handicap 2-way ) to change **rawHandicapValue* :
        DESCRIPTION: Add (change) a value to the filed "Handicap" and save market
        EXPECTED: Handicap value is changed on the selections under the Handicap market without app refresh
        """
        self.__class__.bb_hc_market_template_id = list(self.ob_config.basketball_config.basketball_usa.nba.markets.handicap_2_way.values())[0]
        self.ob_config.change_handicap_market_value(event_id=self.basketball_event_id,
                                                    market_id=self.bb_hc_2_way_market_id,
                                                    market_template_id=self.bb_hc_market_template_id,
                                                    new_handicap_value=self.new_handicap_value)
        self.site.wait_content_state_changed(timeout=30)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        for market_name, market in list(markets_list.items()):
            if market_name == self.handicap_two_way:
                self.handicap_updated_market = market
                break
        self.assertTrue(self.handicap_updated_market, msg=f'Can not find "Handicap 2-way/Spread" market section')
        self.verify_handicap_updates_on_edp()

    def test_003_trigger_the_following_situation_for_this_event_in_ti_for_the_handicap_market_with_3_parameters_handicap_3_way__to_change_rawhandicapvalue_add_change_a_value_to_the_filed_handicap_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Handicap market with 3 parameters (Handicap 3-way ) to change **rawHandicapValue* :
        DESCRIPTION: Add (change) a value to the filed "Handicap" and save market
        EXPECTED: Handicap value is changed on the selections under the Handicap market without app refresh
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        for market_name, market in list(markets_list.items()):
            if self.handicap_three_way in market_name:
                self.handicap_updated_market = market
                break
        self.assertTrue(self.handicap_updated_market, msg=f'Can not find "Handicap 3-way" market section')
        if self.device_type == 'mobile':
            self.handicap_updated_market.click()

        outcome_groups = self.handicap_updated_market.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')
        selection = 1
        number_of_selection = 1
        for outcome_group_name, outcome_group in list(outcome_groups.items()):
            self.outcomes = outcome_group
            h_value = re.findall('[+-]?\d*\.?\d+', outcome_group_name)
            h_value_1 = (h_value[0])
            handicap_sigh, handicap_value = h_value_1[:1], h_value_1[1:]
            if selection == 1:
                self.__class__.old_handicap_value_selection_1 = '%s%s' % (
                    handicap_sigh, '%.1f' % (float(handicap_value)))
                if number_of_selection == 1:
                    self.__class__.market_id_selection_1 = self.ob_config.market_ids[self.basketball_event_id][
                        f'handicap_3_way {self.old_handicap_value_selection_1}']
                    break

        self.__class__.bb_hc_market_template_id = list(self.ob_config.basketball_config.basketball_usa.nba.markets.handicap_3_way.values())[0]
        self.ob_config.change_handicap_market_value(event_id=self.basketball_event_id,
                                                    market_id=self.market_id_selection_1,
                                                    market_template_id=self.bb_hc_market_template_id,
                                                    new_handicap_value=self.new_handicap_value)
        self.site.wait_content_state_changed(timeout=30)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        for market_name, market in markets_list.items():
            if self.handicap_three_way in market_name:
                self.handicap_updated_market = market
                break
        self.handicap_updated_market.click()
        self.assertTrue(self.handicap_updated_market, msg='*** Can not find "Handicap 3 way" market section')
        self.verify_handicap_updates_on_edp()

    def test_004_trigger_the_following_situation_for_this_event_in_ti_for_the_total_points_market_to_change_rawhandicapvalue_add_change_a_value_to_the_filed_higherlower_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Total Points market to change **rawHandicapValue* :
        DESCRIPTION: Add (change) a value to the filed "Higher/lower" and save market
        EXPECTED: Handicap value is changed on the selections under the Total Points market without app refresh
        """
        self.__class__.bb_tp_market_template_id = self.ob_config.basketball_config.basketball_autotest.basketball_autotest_total_points.market_template_id
        self.ob_config.change_handicap_market_value(event_id=self.basketball_event_id,
                                                    market_id=self.bb_total_points_market_id,
                                                    market_template_id=self.bb_tp_market_template_id,
                                                    new_handicap_value=self.new_handicap_value)
        self.site.wait_content_state_changed(timeout=30)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        if self.brand == 'bma':
            self.__class__.total_points = 'Total Points' if self.device_type == 'desktop' else 'TOTAL POINTS'
        else:
            self.__class__.total_points = 'Total Points'
        for market_name, market in markets_list.items():
            if market_name == self.total_points:
                self.handicap_updated_market = market
                break
        self.handicap_updated_market.click()
        self.assertTrue(self.handicap_updated_market, msg='*** Can not find "Total Points" market section')
        self.verify_handicap_updates_on_edp()

    def test_005_open_event_details_page_of_the_in_play_rugby_event_having_setup_described_in_pre_conditions(self):
        """
        DESCRIPTION: Open event details page of the In Play Rugby event having setup described in pre-conditions
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.rugby_event_id)
        self.site.wait_content_state(state_name='EventDetails', timeout=20)
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.siteserve.EXPECTED_MARKET_TABS.all_markets,
                         msg=f'\nCurrent tab: "{current_tab}" '
                             f'is not as expected: "{vec.siteserve.EXPECTED_MARKET_TABS.all_markets}')
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        for market_name, market in markets_list.items():
            if market_name == self.handicap_two_way:
                self.handicap_updated_market = market
                break
        self.assertTrue(self.handicap_updated_market, msg='*** Can not find "Handicap 2-way/Spread" market section')
        outcome_groups = self.handicap_updated_market.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')

    def test_006_trigger_the_following_situation_for_this_event_in_ti_for_the_handicap_market_to_change_rawhandicapvalue_add_change_a_value_to_the_filed_handicap_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Handicap market to change **rawHandicapValue* :
        DESCRIPTION: Add (change) a value to the filed "Handicap" and save market
        EXPECTED: Handicap value is changed on the selections under the Handicap market without app refresh
        """
        rugby_hc_market_template_id = list(self.ob_config.rugby_league_config.rugby_league_all_rugby_league.super_league.markets.handicap_2_way.values())[0]
        self.ob_config.change_handicap_market_value(event_id=self.rugby_event_id,
                                                    market_id=self.rugby_hc_2_way_market_id,
                                                    market_template_id=rugby_hc_market_template_id,
                                                    new_handicap_value=self.new_handicap_value)
        self.site.wait_content_state_changed(timeout=20)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        for market_name, market in list(markets_list.items()):
            if market_name == self.handicap_two_way:
                self.handicap_updated_market = market
                break
        self.assertTrue(self.handicap_updated_market, msg=f'Can not find "{self.handicap_updated_market}" market section')
        self.verify_handicap_updates_on_edp()

    def test_007_trigger_the_following_situation_for_this_event_in_ti_for_the_total_match_points_market_to_change_rawhandicapvalueadd_change_a_value_to_the_filed_higherlower_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Total Match Points market to change **rawHandicapValue*:
        DESCRIPTION: Add (change) a value to the filed "Higher/lower" and save market
        EXPECTED: Handicap value is changed on the selections under the Total Match Points market without app refresh
        """
        rugby_tmp_market_template_id = list(self.ob_config.rugby_league_config.rugby_league_all_rugby_league.super_league.markets.handicap_2_way.values())[0]
        self.ob_config.change_handicap_market_value(event_id=self.rugby_event_id,
                                                    market_id=self.rugby_tmp_market_id,
                                                    market_template_id=rugby_tmp_market_template_id,
                                                    new_handicap_value=self.new_handicap_value)
        self.site.wait_content_state_changed(timeout=30)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        for market_name, market in list(markets_list.items()):
            if market_name == self.handicap_two_way:
                self.handicap_updated_market = market
                break
        self.assertTrue(self.handicap_updated_market, msg=f'Can not find "{self.handicap_updated_market}" market section')
        self.handicap_updated_market.click()
        self.verify_handicap_updates_on_edp()

    def test_008_open_event_details_page_of_the_in_play_cricket_event_having_setup_described_in_pre_conditions(self):
        """
        DESCRIPTION: Open event details page of the In Play Cricket event having setup described in pre-conditions
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.cricket_event_id)
        self.site.wait_content_state(state_name='EventDetails', timeout=20)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        if self.brand == 'bma':
            self.__class__.total_runs = 'Team Runs (Main)' if self.device_type == 'desktop' else 'TEAM RUNS (MAIN)'
        else:
            self.__class__.total_runs = 'Team Runs (Main)'
        for market_name, market in markets_list.items():
            if market_name == self.total_runs:
                self.handicap_updated_market = market
                break
        self.assertTrue(self.handicap_updated_market, msg='*** Can not find Team Runs (Main) market section')
        self.handicap_updated_market.click()
        outcome_groups = self.handicap_updated_market.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')

    def test_009_trigger_the_following_situation_for_this_event_in_ti_for_the_total_runs_player_or_team_runs_or_player_runs_market_to_change_rawhandicapvalueadd_change_a_value_to_the_filed_higherlower_and_save_market(self):
        """
        DESCRIPTION: Trigger the following situation for this event in TI for the Total runs player (or Team runs or Player runs) market to change **rawHandicapValue*:
        DESCRIPTION: Add (change) a value to the filed "Higher/lower" and save market
        EXPECTED: Handicap value is changed on the selections under the Total runs player (or Team runs or Player runs) market without app refresh
        """
        cricket_hc_market_template_id = list(self.ob_config.cricket_config.cricket_all_cricket.cricket_autotest.markets.team_runs.values())[0]
        self.ob_config.change_handicap_market_value(event_id=self.cricket_event_id,
                                                    market_id=self.cricket_hc_2_way_market_id,
                                                    market_template_id=cricket_hc_market_template_id,
                                                    new_handicap_value=self.new_handicap_value)
        self.site.wait_content_state_changed(timeout=30)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'Market list is not displayed')
        for market_name, market in markets_list.items():
            if market_name == self.total_runs:
                self.handicap_updated_market = market
                break
        self.assertTrue(self.handicap_updated_market, msg='*** Can not find Team Runs (Main) market section')
        self.verify_handicap_updates_on_edp()

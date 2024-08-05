import time

import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.google_analytics
@pytest.mark.market_selector
@pytest.mark.markets
@pytest.mark.other
@pytest.mark.low
@vtest
class Test_C360236_tracking_market_selector_inplay(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C360236
    VOL_ID: C9690262
    NAME: Verify Market Selector Tracking on In-Play page
    """
    keep_browser_open = True

    markets = {
        vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_1_5: 'Total Goals Over/Under 1.5',
        vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5: 'Total Goals Over/Under 2.5',
        vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_3_5: 'Total Goals Over/Under 3.5',
        vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_4_5: 'Total Goals Over/Under 4.5',
        vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score: 'Both Teams to Score',
        vec.siteserve.EXPECTED_MARKETS_NAMES.draw_no_bet: 'Draw No Bet',
        vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result: '1st Half Result',
        vec.siteserve.EXPECTED_MARKETS_NAMES.next_team_to_score: 'Next Team to Score',
        vec.siteserve.EXPECTED_MARKETS_NAMES.extra_time_result: 'Extra Time Result',
        vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify: 'To Qualify'}

    total_goals_markets = {vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_1_5: {'over_under': 1.5},
                           vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5: {'over_under': 2.5},
                           vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_3_5: {'over_under': 3.5},
                           vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_4_5: {'over_under': 4.5}}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Adds football events with different markets
        """
        start_time = self.get_date_time_formatted_string(seconds=5)
        if self.brand == 'ladbrokes':
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_1_5] = 'Over/Under Total Goals 1.5'
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5] = 'Over/Under Total Goals 2.5'
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_3_5] = 'Over/Under Total Goals 3.5'
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_4_5] = 'Over/Under Total Goals 4.5'
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result] = 'First-Half Result'
            self.markets[vec.siteserve.EXPECTED_MARKETS_NAMES.extra_time_result] = 'Extra-Time Result'

        for market_name, market_properties in self.total_goals_markets.items():
            over_under = market_properties['over_under']
            self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time,
                                                                      markets=[('over_under_total_goals',
                                                                                {'cashout': True,
                                                                                 'over_under': over_under})])
        self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time,
                                                                  markets=[
                                                                      ('both_teams_to_score', {'cashout': True}),
                                                                      ('draw_no_bet', {'cashout': True}),
                                                                      ('first_half_result', {'cashout': True}),
                                                                      ('to_qualify', {'cashout': True}),
                                                                      ('next_team_to_score', {'cashout': True}),
                                                                      ('extra_time_result', {'cashout': True})])
        self.__class__.category_id = self.ob_config.football_config.category_id

    def test_001_tap_in_play_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'FOOTBALL' icon on the Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_tap_in_play(self):
        """
        DESCRIPTION: Tap on In-Play Module header
        """
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, self.category_id, raise_exceptions=False)

        if not in_play_tab or in_play_tab not in self.site.football.tabs_menu.items_as_ordered_dict:
            inplay_section = self.site.football.tab_content.in_play_module.items_as_ordered_dict
        else:
            self.site.football.tabs_menu.click_button(in_play_tab)
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, in_play_tab,
                             msg=f'"{in_play_tab}" tab is not active, active is "{active_tab}"')
            inplay_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict

        self.assertTrue(inplay_section, msg=f'In-Play module/section is not found')

    def test_003_verify_filtered_events(self):
        """
        DESCRIPTION: Verify "Market Selector" tracking for In-Play page
        """
        for market_name, market_name_in_response in self.markets.items():
            selector = self.site.football.tab_content.dropdown_market_selector
            selector.scroll_to()
            selector.value = market_name
            actual = self.site.inplay.tab_content.dropdown_market_selector.value
            self.assertEqual(actual, market_name,
                             msg=f'Selected market selector "{actual}" is not the same as expected "{market_name}"')
            self.site.inplay.tab_content.dropdown_market_selector.scroll_to()
            self.expected_market_selector_response['categoryID'] = self.ob_config.backend.ti.football.category_id
            self.expected_market_selector_response['eventLabel'] = market_name_in_response
            actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                                  object_value='change market')
            self.compare_json_response(actual_response, self.expected_market_selector_response)
            time.sleep(5)  # need because of compare_json_response works faster than dropdown_market closed

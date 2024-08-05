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
@pytest.mark.google_analytics
@pytest.mark.market_selector
@pytest.mark.markets
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C360236_tracking_market_selector_landing(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C360236
    VOL_ID: C9698367
    NAME: Verify Market Selector Tracking on Sport page
    DESCRIPTION: This test case verifies Market Selector Tracking
    """
    keep_browser_open = True
    event_both_teams_to_score = None

    markets = [vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5,
               vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score,
               vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_and_both_teams_to_score,
               vec.siteserve.EXPECTED_MARKETS_NAMES.draw_no_bet,
               vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result,
               vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Adds football event with different markets
        """
        self.ob_config.add_autotest_premier_league_football_event(markets=[
            ('over_under_total_goals', {'cashout': True, 'over_under': 2.5}),
            ('both_teams_to_score', {'cashout': True}),
            ('draw_no_bet', {'cashout': True}),
            ('first_half_result', {'cashout': True}),
            ('to_qualify', {'cashout': True}),
            ('to_win_to_nil', {'cashout': True}),
            ('match_result_and_both_teams_to_score', {'cashout': True})
        ])

    def test_001_tap_football(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_verify_filtered_events(self):
        """
        DESCRIPTION: Verify "Market Selector" tracking
        """
        self.expected_market_selector_response['categoryID'] = self.ob_config.backend.ti.football.category_id

        for market_name in self.markets:
            market_dropdown = self.site.football.tab_content.dropdown_market_selector
            market_dropdown.value = market_name
            self.expected_market_selector_response['eventLabel'] = market_name
            actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                                  object_value='change market')
            self.compare_json_response(actual_response, self.expected_market_selector_response)
            time.sleep(2)  # need because of compare_json_response works faster than dropdown_market closed

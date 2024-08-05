import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.greyhounds
@vtest
class Test_C60094963_Verify_the_display_of_More_Markets_not_displayed(Common):
    """
    TR_ID: C60094963
    NAME: Verify the display of More Markets- not displayed
    DESCRIPTION: Verify that 'More Markets' tab is no longer displayed in both HR/GH event display page and all the markets previously displayed under More markets tab- Insurance markets are displayed as individual tabs in EDP
    PRECONDITIONS: 1. Horse racing and Grey Hound racing events & markets should be available.
    """
    keep_browser_open = True
    markets = [('win_only',),
               ('betting_without',),
               ('to_finish_second',),
               ('insurance_2_places',),
               ('insurance_3_places',),
               ('top_2_finish',)]

    def test_000_preconditions(self):
        """
        DESCRIPTION: create events
        """
        self.__class__.horseracing_event = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=1)
        self.__class__.greyhound_event = self.ob_config.add_UK_greyhound_racing_event(markets=self.markets, number_of_runners=1)

    def test_001_1launch_coral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: 1:Launch Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('homepage')

    def test_002_2_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: 2: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        self.site.open_sport(name=vec.SB.HORSERACING.upper())

    def test_003_click_on_any_event_which_has_insurance_markets_available(self):
        """
        DESCRIPTION: Click on any event which has Insurance markets available
        EXPECTED: User should be navigated to EDP
        """
        self.navigate_to_edp(event_id=self.horseracing_event.event_id, sport_name='horse-racing')

    def test_004_validate_more_markets_is_not_displayed(self, expected_tabs=None):
        """
        DESCRIPTION: Validate More Markets is not displayed
        EXPECTED: 1: More Markets is not displayed
        EXPECTED: 2: All the Markets are displayed as per their ranking
        """
        if expected_tabs:
            market_tabs = expected_tabs
        else:
            market_tabs = list(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.
                               items_as_ordered_dict.keys())
        self.assertNotIn(vec.racing.RACING_EDP_MARKET_TABS.more_markets, market_tabs, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.more_markets}" tab is present')
        racing_edp_market_list = self.cms_config.get_markets_with_description()
        new_markets_order = [market['name'] for market in racing_edp_market_list]
        for index, item in enumerate(new_markets_order):
            if item.upper() == vec.racing.RACING_EDP_WIN_OR_EACH_WAY_FULL_NAME:
                new_markets_order[index] = 'WIN OR E/W'
        market_index = 0
        order_flag = None
        for market in market_tabs:
            for index, item in enumerate(new_markets_order):
                if item.upper() == market.upper():
                    if index >= market_index:
                        order_flag = True
                        market_index = index
                    else:
                        order_flag = False
                    break
        self.assertTrue(order_flag, msg=f'Actual market list "{market_tabs}" is not the same as expected "{new_markets_order}"')

    def test_005_navigate_to_grey_hounds_and_validate_the_same(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Validate the same
        """
        self.navigate_to_page('homepage')
        self.site.open_sport(name=vec.sb.GREYHOUND.upper())
        self.navigate_to_edp(event_id=self.greyhound_event.event_id, sport_name='greyhound-racing')
        tabs = list(self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.
                    items_as_ordered_dict.keys())
        self.test_004_validate_more_markets_is_not_displayed(expected_tabs=tabs)

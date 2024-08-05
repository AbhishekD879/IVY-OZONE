import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870206_Verify_user_is_able_to_navigate_to_different_sports_pages_and_verify_EDP_fixture(Common):
    """
    TR_ID: C44870206
    NAME: "Verify  user is able to navigate to different sports pages and verify EDP fixture
    DESCRIPTION: "Verify that for different sports pages, user is able to navigate to EDP.
    DESCRIPTION: User is displayed with tabs that order markets upon features, depending on sport specific.
    DESCRIPTION: Generally first tabs are All Markets, Main Markets,
    DESCRIPTION: Under each tab, the markets are listed as headers and selection expand on tap, displaying data and odds as per market specific design.
    DESCRIPTION: User is able to switch between markets and navigate forward and backward, in a smooth journey, and pages functionality works fine
    """
    keep_browser_open = True

    def navigate_to_az_sports(self):
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        all_items.get(vec.sb.ALL_SPORTS).click()
        self.site.wait_content_state(state_name='AllSports')
        self.az_sport_links = self.site.all_sports.a_z_sports_section.items_as_ordered_dict

    def test_001_launch_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Launch https://beta-sports.coral.co.uk/
        EXPECTED: Home page is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_verify_that_for_football_sports_page_user_is_able_to_navigate_to_edp(self):
        """
        DESCRIPTION: Verify that for football sports page, user is able to navigate to EDP.
        EXPECTED: Navigated successfully
        """
        if self.device_type == 'mobile':
            self.site.open_sport(name='FOOTBALL')
        else:
            self.site.header.sport_menu.items_as_ordered_dict[vec.Football.FOOTBALL_TITLE.upper()].click()
        self.site.wait_content_state(state_name='FOOTBALL')
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
        self.navigate_to_edp(self.eventID)
        self.site.wait_splash_to_hide(5)

    def test_003_verify_user_is_displayed_with_tabs_that_order_markets_upon_features_depending_on_sport_specificgenerally_first_tabs_are_all_markets_main_markets(self):
        """
        DESCRIPTION: Verify User is displayed with tabs that order markets upon features, depending on sport specific.
        DESCRIPTION: Generally first tabs are All Markets, Main Markets
        EXPECTED: Other markets tabs are displayed
        EXPECTED: All markets tab is highlighted
        """
        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
        default_tab = self.get_default_tab_name_on_sports_edp(event_id=self.eventID)
        for tab_name, tab in self.markets_tabs_list.items():
            self.assertTrue(tab.is_displayed(), msg=f'"{tab_name}" is not displayed')
            if tab_name == default_tab:
                self.assertTrue(tab.is_selected(timeout=3), msg=f'"{default_tab}" tab is not selected by default')
        self.site.wait_splash_to_hide(5)

    def test_004_under_each_tab_the_markets_are_listed_as_headers_and_selection_expand_on_tap_displaying_data_and_odds_as_per_market_specific_design(self):
        """
        DESCRIPTION: Under each tab, the markets are listed as headers and selection expand on tap, displaying data and odds as per market specific design.
        EXPECTED: Specific markets are displayed for specific market tabs
        """
        for tab_name, tab in self.markets_tabs_list.items():
            if tab_name in [vec.sb.TABS_NAME_MAIN.upper(), vec.sb.TABS_NAME_MAIN_MARKETS.upper(),
                            vec.sb.TABS_NAME_HALF.upper(), vec.sb.TABS_NAME_HALF_MARKETS.upper(),
                            vec.sb.TABS_NAME_ALL_MARKETS.upper()]:
                if not tab.is_selected():
                    tab.click()
                    self.assertTrue(self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[tab_name].is_selected(timeout=5),
                                    msg=f'navigation to the expected tab link "{tab_name}" is not successful')
                markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(markets, msg='markets are not listed')
                for market_name, market in list(markets.items())[0:2] if len(markets) > 2 else markets.items():
                    if not market.is_expanded():
                        market.click()
                        self.assertTrue(market.is_expanded(), msg=f'market "{market_name}" is not expanded by tapping')
                    try:
                        sel_names = list(market.outcomes.items_as_ordered_dict.keys())
                        self.assertTrue(sel_names, msg=f'odds and data for market "{market_name}" is not displayed')
                    except Exception:
                        self._logger.info('cannot find odds items as it is "YOURCALL Market"')

    def test_005_user_is_able_to_switch_between_markets_and_navigate_forward_and_backward_in_a_smooth_journey_and_pages_functionality_works_fine(self):
        """
        DESCRIPTION: User is able to switch between markets and navigate forward and backward, in a smooth journey, and pages functionality works fine
        EXPECTED: navigated successfully
        """
        for tab_name, tab in self.markets_tabs_list.items():
            if not tab.is_selected():
                tab.click()
                self.assertTrue(self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[tab_name].is_selected(),
                                msg=f'navigation to forward tab "{tab_name}" is not successful')
        for tab_name, tab in list(self.markets_tabs_list.items())[::-1]:
            if not tab.is_selected():
                tab.click()
                self.assertTrue(self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[tab_name].is_selected(),
                                msg=f'navigation to backward tab "{tab_name}" is not successful')

    def test_006_verify_that_for_horse_racing_tennis_user_is_able_to_navigate_to_edp_from_a_z_menu(self):
        """
        DESCRIPTION: Verify that for horse racing/ tennis, user is able to navigate to EDP from A-Z menu
        EXPECTED: Navigated successfully to the respective pages.
        """
        self.navigate_to_page('Homepage')
        if self.device_type == 'mobile':
            self.navigate_to_az_sports()
        else:
            self.az_sport_links = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
        for sport in ['Horse Racing', 'Tennis']:
            if self.device_type == 'mobile':
                try:
                    self.az_sport_links = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
                except Exception:
                    self.navigate_to_az_sports()
            else:
                self.az_sport_links = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.az_sport_links[sport].click()
            if sport == 'Horse Racing':
                if tests.settings.backend_env == 'prod':
                    event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
                    eventID = event['event']['id']
                else:
                    event_params = self.ob_config.add_UK_racing_event()
                    eventID = event_params.event_id
                self.navigate_to_edp(eventID, 'horse-racing')
            else:
                if tests.settings.backend_env == 'prod':
                    event = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id)[0]
                    eventID = event['event']['id']
                else:
                    event_params = self.ob_config.add_tennis_event_to_autotest_trophy()
                    eventID = event_params.event_id
                self.navigate_to_edp(eventID)
            self.navigate_to_page('Homepage')

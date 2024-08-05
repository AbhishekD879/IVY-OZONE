import pytest
import tests
from time import sleep
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.time_league_filters
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60035083_Verify_interaction_between_Market_switcher_and_Time_Frame_for_Tier_1_sports(Common):
    """
    TR_ID: C60035083
    NAME: Verify interaction between Market switcher and Time Frame for Tier 1 sports
    DESCRIPTION: This test case verifies interaction between the Market switcher and Time Frame for Tier 1 sports
    """
    keep_browser_open = True
    both_teams_to_score_market = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
    added_filters = ['1h', '2h', '3h', '6h', '12h', '21h', '24h', '48h']

    def verify_events_are_sorted_by_time(self):
        """
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        event_time_list = []
        sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(sections) > 0:
            for league in sections:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    event_template = event.template
                    self.assertTrue(event_template.event_time.split(" ")[0],
                                    msg=f'"Event time" not displayed')
                    event_time_list.append(event_template.event_time.split(" ")[0])

            self.assertListEqual(sorted(event_time_list), sorted(event_time_list),
                                 msg=f'Actual event time  "{sorted(event_time_list)}"'
                                     f' is not matching with expected list "{sorted(event_time_list)}"')
        else:
            no_events = self.site.contents.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def navigate_to_league(self, league_category, league_name):

        if tests.settings.backend_env != 'prod':
            if self.device_type == 'desktop':
                self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[
                    vec.sb_desktop.COMPETITIONS_SPORTS].click()
                competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            else:
                competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(competitions, msg='No competitions are present on page')

        if self.device_type == 'mobile':
            category = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict.get(
                league_category)
        else:
            category = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(league_category)
        self.assertTrue(category, msg='category is not displayed')
        if not category.is_expanded():
            category.expand()
        league = wait_for_result(lambda: category.items_as_ordered_dict.get(league_name), timeout=10)
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage', timeout=30)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
        PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
        PRECONDITIONS: - Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
        PRECONDITIONS: - 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Competitions)
        PRECONDITIONS: - The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours(Sports Pages > Sports Categories > Sport > Competitions)
        PRECONDITIONS: **Designs**
        PRECONDITIONS: Mobile
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
        PRECONDITIONS: Desktop
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Navigate to Tier1 Sport Landing page
        PRECONDITIONS: 3. Click/Tap on the 'Competition' tab
        """
        if tests.settings.backend_env != 'prod':
            markets = [
                ('to_qualify',),
                ('over_under_total_goals', {'over_under': 2.5}),
                ('both_teams_to_score',),
                ('draw_no_bet',),
                ('first_half_result',)
            ]
            self.ob_config.add_autotest_premier_league_football_event(markets=markets, is_live=True)
            self.ob_config.add_football_event_to_england_championship()
            all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                           status=True)
            self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sport')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='football',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for football sport')

            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')

            sport_event_filters_enable = self.cms_config.get_system_configuration_structure()['FeatureToggle'][
                'SportEventFilters']

            if not sport_event_filters_enable:
                self.cms_config.update_system_configuration_structure(config_item='Feature Toggle',
                                                                      field_name='SportEventFilters',
                                                                      field_value=True)

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            sport_id=self.ob_config.football_config.category_id,
            enabled=True, event_filters_values=[1, 3, 6, 12, 24, 48])

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.football_config.category_id,
            enabled=True, event_filters_values=[1, 3, 6, 12, 24, 48])

        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='football')
        self.__class__.expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                                    self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(self.expected_sport_tab)
        self.site.wait_content_state_changed()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

    def test_001_clicktap_on_some_league(self):
        """
        DESCRIPTION: Click/Tap on some League
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        if tests.settings.backend_env != 'prod':
            if self.device_type == 'desktop':
                self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[
                    vec.sb_desktop.COMPETITIONS_SPORTS].click()
                competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            else:
                competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(competitions, msg='No competitions are present on page')

            if self.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = 'Auto Test'
                self.navigate_to_league(league_category=league,
                                        league_name=vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME)
            else:
                league = 'AUTO TEST'
                self.navigate_to_league(league_category=league, league_name=vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME)
        else:
            if self.brand == 'ladbrokes' and self.device_type == 'desktop':
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(),
                                        league_name=vec.siteserve.PREMIER_LEAGUE_NAME)
            else:
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND,
                                        league_name=vec.siteserve.PREMIER_LEAGUE_NAME)

        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertIsNone(selected_filters, msg="Filter is already selected")
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        for filter_name, filter_loc in filters.items():
            self.assertIn(filter_name, self.added_filters, msg="Filter is not added")

    def test_002_select_filter_eg_3_hours(self, tfilter="3h"):
        """
        DESCRIPTION: Select filter, e.g. 3 hours
        EXPECTED: - Page loads only events that are due to start within the next 3 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict[tfilter].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], tfilter,
                         msg=f'"selected time filter {list(selected_filters.keys())[0]} "'
                             f'does not match expected time filter {tfilter}')
        self.assertEqual(list(selected_filters.keys())[0], tfilter,
                         msg=f'"selected time filter {list(selected_filters.keys())[0]} "'
                             f'does not match expected time filter {tfilter}')
        self.verify_events_are_sorted_by_time()
        selected_color = self.site.sports_page.tab_content.timeline_filters.selected_filter.background_color_value
        self.assertEqual(selected_color, vec.colors.SHOW_INFO_COLOR,
                         msg=f'Time Filter actual color "{selected_color}"'
                             f' is not highlighted in blue as expected color '
                             f'"{vec.colors.SHOW_INFO_COLOR}"')

    def test_003_change_market_from_market_selector(self):
        """
        DESCRIPTION: Change market from Market Selector
        EXPECTED: - Markets update to reflect the change in market, in line with the time/league filter selected by user
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        EXPECTED: - Selected market is displayed
        """
        if self.brand == 'ladbrokes':
            self.__class__.market_selector_default_value = 'Match Result' if self.device_type == 'mobile' else 'MATCH RESULT'
        else:
            self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result

        football_tab_content = self.site.football.tab_content
        has_no_events_label = football_tab_content.has_no_events_label()
        if not has_no_events_label:
            self.assertTrue(football_tab_content.has_dropdown_market_selector(),
                            msg='"Market Selector" drop-down is not displayed on Football landing page')
            selected_item = football_tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_item,
                             self.market_selector_default_value,
                             msg=f'Incorrect market name is selected by default:\n'
                                 f'Actual: {selected_item}\n Expected: {self.market_selector_default_value}')

            market_dropdown = football_tab_content.dropdown_market_selector
            if self.device_type == 'mobile':
                market_dropdown.click()
            market_dropdown.value = self.both_teams_to_score_market
            sleep(3)
            if self.brand == 'ladbrokes' and self.device_type != 'mobile':
                self.both_teams_to_score_market = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score.upper()
            selected_item = football_tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_item, self.both_teams_to_score_market,
                             msg=f'Incorrect market name is selected by default:\n'
                                 f'Actual: {selected_item}\n Expected: {self.both_teams_to_score_market}')
            selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
            self.assertTrue(selected_filters, msg="Filter is not already selected")
        else:
            self.assertTrue(football_tab_content.has_no_events_label(),
                            msg='"no event label" not displayed selected market has events ')

    def test_004_change_market_from_market_selector_where_no_events_present_or_events_from_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change market from Market Selector, where no events present or events from selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        # Covered in above step

    def test_005_switch_tab_eg_to_sport_landing_page_or_to_in_play_page(self):
        """
        DESCRIPTION: Switch tab, e.g. to Sport Landing page or to In-Play page
        EXPECTED: Filtering by time and market would not be applied to newly selected tab
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        football_tab_content = self.site.football.tab_content
        has_no_events_label = football_tab_content.has_no_events_label()
        if not has_no_events_label:
            self.assertTrue(football_tab_content.has_dropdown_market_selector(),
                            msg='"Market Selector" drop-down is not displayed on Football landing page')
            selected_item = football_tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_item.upper(),
                             self.market_selector_default_value.upper(),
                             msg=f'Incorrect market name is selected by default:\n'
                                 f'Actual: {selected_item}\n Expected: {self.market_selector_default_value}')

            selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
            self.assertIsNone(selected_filters,
                              msg="Filtering is applied to newly selected tab")
        else:
            self.assertTrue(football_tab_content.has_no_events_label(),
                            msg='"no event label" not displayed selected market has events ')

    def test_006_tapclick_back_into_competitions(self):
        """
        DESCRIPTION: Tap/Click back into Competitions
        EXPECTED: Filtering by time and market that previously applied is reset
        """
        self.site.football.tabs_menu.click_button(self.expected_sport_tab)
        self.site.wait_content_state_changed()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')
        self.test_001_clicktap_on_some_league()

    def test_007_change_market_from_market_selector(self):
        """
        DESCRIPTION: Change market from Market Selector
        EXPECTED: Markets update to reflect the change in market
        """
        football_tab_content = self.site.football.tab_content
        has_no_events_label = football_tab_content.has_no_events_label()
        if not has_no_events_label:
            self.assertTrue(football_tab_content.has_dropdown_market_selector(),
                            msg='"Market Selector" drop-down is not displayed on Football landing page')
            selected_item = football_tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_item.upper(),
                             self.market_selector_default_value.upper(),
                             msg=f'Incorrect market name is selected by default:\n'
                                 f'Actual: {selected_item}\n Expected: {self.market_selector_default_value}')
            markets = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
            self.assertTrue(markets, msg='No markets available in the market switcher dropdown')
            if not self.both_teams_to_score_market in markets:
                raise VoltronException('expected market not available')
            else:
                market = markets.get(self.both_teams_to_score_market)
                market.click()
                sleep(5)
                selected_market = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
                self.assertEqual(selected_market.upper(), self.both_teams_to_score_market.upper(),
                                 msg=f'Actual Market: "{selected_market.upper()}" is not same as'
                                     f'Expected Market: "{self.both_teams_to_score_market.upper()}",'
                                     f'Market selector functionality is not working')


    def test_008_select_filter_eg_12_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 12 hours
        EXPECTED: - Events update to be in line with filter selected as well as the market selected by user
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        EXPECTED: - Selected market is displayed
        """
        self.test_002_select_filter_eg_3_hours(tfilter='12h')

    def test_009_change_time_filter_where_events_from_the_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change Time Filter, where events from the selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        football_tab_content = self.site.football.tab_content
        has_no_events_label = football_tab_content.has_no_events_label()
        if has_no_events_label:
            self.assertTrue(football_tab_content.has_no_events_label(),
                            msg='"no event label" not displayed selected market has events ')
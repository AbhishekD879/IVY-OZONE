import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.time_league_filters
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60063988_Verify_interaction_between_League_Filters_and_Market_switcher(Common):
    """
    TR_ID: C60063988
    NAME: Verify interaction between League Filters and Market switcher
    DESCRIPTION: This Test Case verifies interaction between League Filters and Market switcher
    PRECONDITIONS: * 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: Designs for filters:
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
    PRECONDITIONS: **League Filters are available for Desktop only on Today Tab**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page
    """
    keep_browser_open = True

    event_markets = [
        ('sixty_minutes_betting',),
        ('puck_line',),
        ('total_goals_2_way',)]

    basketball_event_markets = [
        ('total_points',),
        ('handicap_2_way',),
        ('home_team_total_points',),
        ('away_team_total_points',)]

    def verify_events_sorted_by_time(self, selected_filter=True):
        event_time_list = []
        sections = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        if selected_filter:
            if len(sections) > 0:
                for league in sections[:3]:
                    if not league.is_expanded():
                        league.expand()
                    sleep(5)
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
        else:
            if len(sections) > 0:
                events = list(sections[0].items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    event_template = event.template
                    is_live = event_template.is_live_now_event
                    if is_live:
                        self._logger.info(f'{event_template.event_name} is live event')
                    else:
                        self.assertTrue(event_template.event_time,
                                        msg=f'"Event time" not displayed')
            else:
                no_events = self.site.contents.tab_content.has_no_events_label()
                self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
        PRECONDITIONS: Notes:
        PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
        PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
        PRECONDITIONS: Designs for filters:
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
        PRECONDITIONS: **League Filters are available for Desktop only on Today Tab**
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Navigate to Sports Landing page
        """
        if tests.settings.backend_env != 'prod':
            icehockey_event = self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets,
                                                                                    start_time=self.get_date_time_formatted_string(
                                                                                        hours=3))
            basketball_event = self.ob_config.add_basketball_event_to_us_league(markets=self.basketball_event_markets)
            self.__class__.ice_hockey_type_id = icehockey_event.ss_response['event']['typeId']
            self.__class__.basketball_type_id = basketball_event.ss_response['event']['typeId']
        else:
            icehockey_event = \
                self.get_active_events_for_category(category_id=self.ob_config.ice_hockey_config.category_id)[
                    0]
            self.__class__.ice_hockey_type_id = icehockey_event['event']['typeId']
            basketball_event = \
                self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id)[0]
            self.__class__.basketball_type_id = basketball_event['event']['typeId']
            self.cms_config.verify_and_update_sport_config(
                sport_category_id=self.ob_config.backend.ti.ice_hockey.category_id,
                disp_sort_names='HH,WH,MR,HL',
                primary_markets='|Money Line|,|Total Goals 2-way|,|Puck Line|,|60 Minutes Betting|')

        self.cms_config.verify_and_update_market_switcher_status(sport_name='icehockey',
                                                                 status=True)
        self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                 status=True)
        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.ice_hockey_config.category_id,
            top_league_ids=self.ice_hockey_type_id,
            test_league_ids=self.ice_hockey_type_id,
            invalid_league_ids='1234',
            league_enabled=True,
            enabled=True,
            league_required=True,
            event_filters_values=[1, 3, 6, 12, 24, 48])

        # tier1 basketball
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.basketball.category_id,
            disp_sort_names='HL,WH,HH',
            primary_markets='|Money Line|,|Total Points|,'
                            '|Home team total points|,|Away team total points|,'
                            '|Half Total Points|,|Quarter Total Points|,'
                            '|Handicap 2-way|')
        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.basketball_config.category_id,
            top_league_ids=self.basketball_type_id,
            test_league_ids=self.basketball_type_id,
            invalid_league_ids='1234',
            league_enabled=True,
            enabled=True,
            league_required=True,
            event_filters_values=[1, 3, 6, 12, 24, 48])
        self.site.wait_content_state('HomePage')
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                     self.ob_config.cricket_config.category_id)
        active_tab = self.site.contents.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Matches tab is not active, active is "{active_tab}"')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg=f'Filters are selected or highlighted by default')

    def test_001_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.__class__.filter = list(self.filters.values())
        self.__class__.filter_name = list(self.filters.keys())
        self.assertIn(vec.bma.TOP_LEAGUE, self.filter_name, msg=f'"{vec.bma.TOP_LEAGUE}" not contain '
                                                                f'"{self.filter_name}"')
        self.filter[0].click()
        selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
        self.assertIn(self.filter_name[0], selected_filters, msg=f'Actual "{self.filter_name[0]}"'
                                                                 f' is not same as expected "{selected_filters}"')
        self.verify_events_sorted_by_time()

    def test_002_select_another_market_from_the_market_switcher(self):
        """
        DESCRIPTION: Select another Market from the Market Switcher
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        self.__class__.markets = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No markets available in the market switcher dropdown')
        if len(list(self.markets.keys())) <= 1:
            raise VoltronException('No More than one market')
        else:
            self.__class__.market_name, market = list(self.markets.items())[1]
            market.click()
            sleep(5)
            selected_market = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_market.upper(), self.market_name.upper(),
                             msg=f'Actual Market: "{selected_market.upper()}" is not same as'
                                 f'Expected Market: "{self.market_name.upper()}",'
                                 f'Market selector functionality is not working')
            selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
            self.assertIn(self.filter_name[0], selected_filters, msg=f'Actual "{self.filter_name[0]}"'
                                                                     f' is not same as expected "{selected_filters}"')

            self.verify_events_sorted_by_time()

    def test_003_change_the_market_from_market_selector_where_no_events_present(self):
        """
        DESCRIPTION: Change the market from Market Selector, where no events present
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        # cannot be automatable

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Default Market is displayed in the Market Switcher
        EXPECTED: * Any League Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        self.device.refresh_page()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(selected_filters, None, msg='Some filters are selected by default but expected to be None')

    def test_005_select_another_market_from_the_market_switcher(self):
        """
        DESCRIPTION: Select another Market from the Market Switcher
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Page loads only events that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        self.__class__.markets = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.__class__.market_name, market = list(self.markets.items())[1]
        market.click()
        selected_market = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_market.upper(), self.market_name.upper(),
                         msg=f'Actual Market: "{selected_market.upper()}" is not same as'
                             f'Expected Market: "{self.market_name.upper()}",'
                             f'Market selector functionality is not working')
        self.verify_events_sorted_by_time()

    def test_006_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.__class__.filter = list(self.filters.values())
        self.assertIn(vec.bma.TEST_LEAGUE, self.filter_name, msg=f'"{vec.bma.TEST_LEAGUE}" not contain '
                                                                 f'"{self.filter_name}"')
        self.filter[1].click()
        selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
        self.assertIn(self.filter_name[1], selected_filters,
                      msg=f'Actual "{self.filter_name[1]}" is not same as expected "{selected_filters}"')
        self.assertNotIn(self.filter_name[0], selected_filters, msg=f'Actual "{self.filter_name[0]}"'
                                                                    f' is present "{selected_filters}"')
        self.verify_events_sorted_by_time()

    def test_007_select_invalid_league_filter_or_filter_without_available_events_eg_invalid_league(self):
        """
        DESCRIPTION: Select invalid League Filter or filter without available Events (e.g. 'Invalid League')
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * New selected League Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        self.assertIn(vec.bma.INVALID_LEAGUE, self.filter_name, msg=f'"{vec.bma.INVALID_LEAGUE}" not contain '
                                                                    f'"{self.filter_name}"')
        self.filter[2].click()
        selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
        self.assertIn(self.filter_name[2], selected_filters,
                      msg=f'Actual "{self.filter_name[2]}" is not same as expected "{selected_filters}"')
        self.assertNotIn(self.filter_name[1], selected_filters, msg=f'Actual "{self.filter_name[1]}"'
                                                                    f' is present "{selected_filters}"')
        no_events = self.site.contents.tab_content.has_no_events_label()
        self.assertTrue(no_events, msg=f'"No Events Found" msg not displayed')

    def test_008_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')
        self.test_001_select_some_league_filter_eg_top_leagues()
        self.test_002_select_another_market_from_the_market_switcher()
        self.test_003_change_the_market_from_market_selector_where_no_events_present()
        self.test_004_refresh_the_page()
        self.test_005_select_another_market_from_the_market_switcher()
        self.test_006_select_some_league_filter_eg_top_leagues()
        self.test_007_select_invalid_league_filter_or_filter_without_available_events_eg_invalid_league()

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
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.time_league_filters
@vtest
class Test_C60081185_Verify_interaction_between_Market_Switcher_League_filters_and_Time_Filters(Common):
    """
    TR_ID: C60081185
    NAME: Verify interaction between Market Switcher, League filters and Time Filters
    DESCRIPTION: This test case verifies interaction between Market Switcher, League filters, and Time Filters
    PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: Designs for filters:
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
    PRECONDITIONS: **Time Filters are available for Desktop only up to 12 hours and only on Today Tab**
    PRECONDITIONS: **League Filters are available for Desktop only on Today Tab**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page (Today tab)
    """
    keep_browser_open = True
    twelve_hour_time = '12h'

    cricket_event_markets = [
        ('total_sixes',),
        ('team_runs',),
        ('next_over_runs',),
        ('runs_at_fall_of_next_wicket',)]

    basketball_event_markets = [
        ('total_points',),
        ('handicap_2_way',),
        ('home_team_total_points',),
        ('away_team_total_points',)]

    def verify_events_sorted_by_time(self):
        event_time_list = []
        no_events = self.site.contents.tab_content.has_no_events_label()
        if no_events:
            raise VoltronException('"Events not found" label appeared')
        else:
            sections = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.items())
            for league_name, league in sections:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    event_template = event.template
                    is_live = event_template.is_live_now_event
                    if is_live:
                        self._logger.info(f'{event_template.event_name} is live event')
                    else:
                        self.assertTrue(event_template.event_time.split(" ")[0],
                                        msg=f'"Event time" not displayed')
                        event_time_list.append(event_template.event_time.split(" ")[0])
                self.assertListEqual(event_time_list, sorted(event_time_list),
                                     msg=f'Actual event time  "{event_time_list}"'
                                         f' is not matching with expected list "{sorted(event_time_list)}"')
                event_time_list.clear()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Timefilters should be enabled in CMS
        """
        if tests.settings.backend_env != 'prod':
            cricket_event = self.ob_config.add_autotest_cricket_event(markets=self.cricket_event_markets,
                                                                      start_time=self.get_date_time_formatted_string(hours=12))
            basketball_event = self.ob_config.add_basketball_event_to_us_league(markets=self.basketball_event_markets,
                                                                                start_time=self.get_date_time_formatted_string(hours=12))
            cricket_type_id = cricket_event.ss_response['event']['typeId']
            basketball_type_id = basketball_event.ss_response['event']['typeId']
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.cricket_config.category_id,
                                                           disp_sort_names='MR,HH,WH,HL',
                                                           primary_markets='|Match Betting|,|Match Betting Head/Head|,'
                                                                           '|Total Sixes|,'
                                                                           '|Team Runs (Main)|,|Next Over Runs (Main)|,'
                                                                           '|Runs At Fall Of Next Wicket|')
        else:
            cricket_event = self.get_active_events_for_category(category_id=self.ob_config.cricket_config.category_id)[0]
            cricket_type_id = cricket_event['event']['typeId']
            basketball_event = self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id)[0]
            basketball_type_id = basketball_event['event']['typeId']

        self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket',
                                                                 status=True)
        self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                 status=True)
        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.cricket_config.category_id,
            top_league_ids=cricket_type_id,
            test_league_ids=cricket_type_id,
            invalid_league_ids='1234',
            league_enabled=True,
            enabled=True,
            league_required=True,
            event_filters_values=[1, 3, 6, 12, 24, 48])
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
            top_league_ids=basketball_type_id,
            test_league_ids=basketball_type_id,
            invalid_league_ids='1234',
            league_enabled=True,
            enabled=True,
            league_required=True,
            event_filters_values=[1, 3, 6, 12, 24, 48])
        self.site.wait_content_state('HomePage')
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='cricket')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                     self.ob_config.cricket_config.category_id)
        active_tab = self.site.contents.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Matches tab is not active, active is "{active_tab}"')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg=f'Filters are selected or highlighted by default')

    def test_001_select_some_time_filter_eg_3_hoursselect_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some Time Filter (e.g. 3 hours)
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours AND that in line with 'Top Leagues' League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours AND that in line with 'Top Leagues' League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.__class__.filter = list(self.filters.values())
        self.__class__.filter_name = list(self.filters.keys())
        self.assertIn(vec.bma.TOP_LEAGUE, self.filter_name, msg=f'"{vec.bma.TOP_LEAGUE}" not contain '
                                                                f'"{self.filter_name}"')
        self.filter[0].click()
        sleep(1)
        self.filters.get(self.twelve_hour_time).click()
        sleep(1)
        expected_filters = [self.filter_name[0], self.twelve_hour_time]
        selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
        self.assertEqual(selected_filters, expected_filters,
                         msg=f'Actual time filter: "{selected_filters}" is not same as'
                             f'Expected time filter: "{expected_filters}".')
        self.verify_events_sorted_by_time()

    def test_002_select_another_market_from_the_market_switcher(self):
        """
        DESCRIPTION: Select another Market from the Market Switcher
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * age loads only events (Upcoming Matches List only) that are due to start within the next 3 hours AND that are in line to selected League Filter for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Cricket')
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
            expected_filters = [self.filter_name[0], self.twelve_hour_time]
            selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
            self.assertEqual(selected_filters, expected_filters,
                             msg=f'Actual time filter: "{selected_filters}" is not same as'
                                 f'Expected time filter: "{expected_filters}".')
            self.verify_events_sorted_by_time()

    def test_003_change_the_market_from_market_selector_where_no_events_present(self):
        """
        DESCRIPTION: Change the market from Market Selector, where no events present
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        # cannot be automatable

    def test_004_select_the_previous_market_from_step_2select_invalid_league_filter_or_filter_without_available_events_eg_invalid_league(self):
        """
        DESCRIPTION: Select the previous Market from Step 2
        DESCRIPTION: Select invalid League Filter or filter without available Events (e.g. 'Invalid League')
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * New selected League Filter is highlighted
        EXPECTED: * Selected Time Filter is highlighted
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

    def test_005_select_some_league_filter_eg_top_leaguesselect_some_time_filter_where_events_from_selected_time_frame_arent_available_eg_1_hours(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        DESCRIPTION: Select some Time Filter where events from selected time frame aren't available (e.g. 1 hours)
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * New selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        for time_filter_name, time_filter in list(self.filters.items()):
            time_filter.click()
            no_events = self.site.contents.tab_content.has_no_events_label()
            if no_events:
                self._logger.info(msg='"No events found" message displayed')
                break
            else:
                self._logger.info(msg=f'"No events found" is not found for time filter "{time_filter_name}"')
                continue

    def test_006_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sport(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sport.
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
        self.test_001_select_some_time_filter_eg_3_hoursselect_some_league_filter_eg_top_leagues()
        self.test_002_select_another_market_from_the_market_switcher()
        self.test_004_select_the_previous_market_from_step_2select_invalid_league_filter_or_filter_without_available_events_eg_invalid_league()
        self.test_005_select_some_league_filter_eg_top_leaguesselect_some_time_filter_where_events_from_selected_time_frame_arent_available_eg_1_hours()

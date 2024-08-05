import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
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
class Test_C60035084_Verify_interaction_between_Market_switcher_and_Time_Frame_for_Tier_2_sports(Common):
    """
    TR_ID: C60035084
    NAME: Verify interaction between Market switcher and Time Frame for Tier 2 sports
    DESCRIPTION: This test case verifies interaction between Market switcher and Time Frame for Tier 2 sports
    PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Competitions)
    PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Competitions)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Mobile
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
    PRECONDITIONS: Desktop
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Tier 2 Sports Landing page
    """
    keep_browser_open = True
    three_hour_time = '3h'
    twelve_hour_time = '12h'
    event_markets = [
        ('total_sixes',),
        ('team_runs',),
        ('next_over_runs',),
        ('runs_at_fall_of_next_wicket',)]

    def verify_events_sorted_by_time(self):
        event_time_list = []
        no_events = self.site.contents.tab_content.has_no_events_label()
        if no_events:
            raise VoltronException('"Events not found" label appeared for cricket')
        else:
            sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.items())
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
            self.ob_config.add_autotest_cricket_event(markets=self.event_markets,
                                                      start_time=self.get_date_time_formatted_string(hours=3))
            self.ob_config.add_autotest_cricket_event(markets=self.event_markets,
                                                      start_time=self.get_date_time_formatted_string(hours=12))

            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.cricket_config.category_id,
                                                       disp_sort_names='MR,HH,WH,HL',
                                                       primary_markets='|Match Betting|,|Match Betting Head/Head|,'
                                                                       '|Total Sixes|,'
                                                                       '|Team Runs (Main)|,|Next Over Runs (Main)|,'
                                                                       '|Runs At Fall Of Next Wicket|')
        self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket',
                                                                 status=True)
        self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                 status=True)
        self.cms_config.update_sports_event_filters(tab_name='competitions', sport_id=10, enabled=True,
                                                    event_filters_values=[1, 3, 6, 12, 24, 48])

        self.site.wait_content_state('HomePage')
        self.navigate_to_page(name='sport/cricket')

    def test_001_clicktap_on_the_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on the 'Competition' tab
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        """
        competitions_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                        10)
        self.site.contents.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.contents.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name,
                         msg=f'"{competitions_tab_name}" tab is not active, '
                             f'active is "{active_tab}"')
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        self.assertTrue(has_time_filter, msg='Time filter not available')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg='Time filters selected')

    def test_002_select_filter_eg_3_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 3 hours
        EXPECTED: - Page loads only events that are due to start within the next 3 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.filters.get(self.three_hour_time).click()
        selected_filters = self.site.competition_league.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.three_hour_time,
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.three_hour_time}".')
        self.verify_events_sorted_by_time()

    def test_003_change_market_from_market_selector(self):
        """
        DESCRIPTION: Change market from Market Selector
        EXPECTED: - Markets update to reflect the change in market, in line with the time/league filter selected by user
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        EXPECTED: - Selected market is displayed
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
            selected_filters = self.site.competition_league.tab_content.timeline_filters.selected_filters
            self.assertEqual(list(selected_filters.keys())[0], self.three_hour_time,
                             msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                                 f'Expected time filter: "{self.three_hour_time}".')
            self.verify_events_sorted_by_time()

    def test_004_change_market_from_market_selector_where_no_events_present_or_events_from_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change market from Market Selector, where no events present or events from selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        if len(list(self.markets.values())) > 2:
            self.__class__.markets = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
            for market_name, market in list(self.markets.items())[2:]:
                market_dropdown = self.site.contents.tab_content.dropdown_market_selector
                market_dropdown.click_item(market_name)
                no_events = self.site.contents.tab_content.has_no_events_label()
                if no_events:
                    break
                else:
                    self.__class__.markets = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
                    self._logger.info(msg=f'"Events available" for the market "{market_name}"')
            else:
                self._logger.error(msg='Not found "No events found" message in any market')
        else:
            raise VoltronException('No More than two market')

    def test_005_switch_tab_eg_to_sport_landing_page_or_to_in_play_page(self):
        """
        DESCRIPTION: Switch tab, e.g. to Sport Landing page or to In-Play page
        EXPECTED: Filtering by time and market would not be applied to newly selected tab
        """
        self.navigate_to_page(name='sport/cricket')
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        if has_time_filter:
            selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
            self.assertFalse(selected_filters, msg='Time filters selected')
        else:
            self._logger.info(msg='"Time filters" not available')
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        if has_market_selector:
            selected_market = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertNotEqual(selected_market.upper(), self.market_name.upper(),
                                msg=f'Actual Market: "{selected_market.upper()}" is same as'
                                    f'Expected Market: "{self.market_name.upper()}".')

    def test_006_tapclick_back_into_competitions(self):
        """
        DESCRIPTION: Tap/Click back into Competitions
        EXPECTED: Filtering by time and market that previously applied is reset
        """
        self.test_001_clicktap_on_the_competition_tab()
        selected_market = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertNotEqual(selected_market.upper(), self.market_name.upper(),
                            msg=f'Actual Market: "{selected_market.upper()}" is same as'
                                f'Expected Market: "{self.market_name.upper()}",'
                                f'Market selector functionality is not working')

    def test_007_change_market_from_market_selector(self):
        """
        DESCRIPTION: Change market from Market Selector
        EXPECTED: Markets update to reflect the change in market
        """
        market_dropdown = self.site.contents.tab_content.dropdown_market_selector
        dropdown = market_dropdown.is_expanded()
        if not dropdown:
            market_dropdown = self.site.contents.tab_content.dropdown_market_selector
        markets = market_dropdown.items_as_ordered_dict
        market_name, market = list(markets.items())[-1]
        market.click()
        sleep(3)
        selected_market = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_market.upper(), market_name.upper(),
                         msg=f'Actual Market: "{selected_market.upper()}" is not same as'
                             f'Expected Market: "{market_name.upper()}", Market selector functionality is not working')

    def test_008_select_filter_eg_12_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 12 hours
        EXPECTED: - Events update to be in line with filter selected as well as the market selected by user
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        EXPECTED: - Selected market is displayed
        """
        self.__class__.filters = self.site.competition_league.tab_content.timeline_filters.items_as_ordered_dict
        self.filters.get(self.twelve_hour_time).click()
        selected_filters = self.site.competition_league.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.twelve_hour_time,
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.twelve_hour_time}".')
        self.verify_events_sorted_by_time()

    def test_009_change_time_filter_where_events_from_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change Time Filter, where events from selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
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


import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.time_league_filters_negative
@vtest
class Test_C60037168_Verify_Filtering_on_Competitions_for_Tier_2_Sports_without_Market_Selector(Common):
    """
    TR_ID: C60037168
    NAME: Verify Filtering on Competitions for Tier 2 Sports without Market Selector
    DESCRIPTION: This test case verifies  Filtering on Competitions for Tier 2 Sports without Market Selector
    PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Competitions)
    PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Competitions)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - List of Sports
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Mobile
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
    PRECONDITIONS: Desktop
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page (market selector should be absent for this sport), e.g. Cricket
    """
    keep_browser_open = True
    one_hour_time = '1h'
    six_hour_time = '6h'

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
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=1))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=6))

            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.cricket_config.category_id,
                                                       disp_sort_names='MR,HH,WH,HL',
                                                       primary_markets='|Match Betting|,|Match Betting Head/Head|,'
                                                                       '|Total Sixes|,'
                                                                       '|Team Runs (Main)|,|Next Over Runs (Main)|,'
                                                                       '|Runs At Fall Of Next Wicket|')
        self.cms_config.update_sports_event_filters(tab_name='competitions',
                                                    sport_id=self.ob_config.cricket_config.category_id, enabled=True,
                                                    event_filters_values=[1, 3, 6, 12, 24, 48])
        self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=False)
        self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket', status=False)
        self.site.wait_content_state('HomePage')
        self.navigate_to_page(name='sport/cricket')

    def test_001_clicktap_on_the_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on the 'Competition' tab
        EXPECTED: - Market selector is absent
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.cricket_config.category_id)
        self.site.contents.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.contents.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        self.assertTrue(has_time_filter, msg='Time filter not available')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg='Time filters selected')
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertFalse(has_market_selector, msg=' "Market selector" is available for Cricket')

    def test_002_select_filter_eg_1_hour(self):
        """
        DESCRIPTION: Select filter, e.g. 1 hour
        EXPECTED: - Page loads only events that are due to start within the next 1 hour for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.filters.get(self.one_hour_time).click()
        selected_filters = self.site.competition_league.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.one_hour_time,
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.one_hour_time}".')
        self.verify_events_sorted_by_time()

    def test_003_click_on_the_selected_time_filter_to_remove_highlight(self):
        """
        DESCRIPTION: Click on the selected time filter to remove highlight
        EXPECTED: User returns to the default view
        """
        self.filters.get(self.one_hour_time).click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg='Time filters are selected')

    def test_004_select_filter_eg_6_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 6 hours
        EXPECTED: - Page loads only events that are due to start within the next 6 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        self.filters.get(self.six_hour_time).click()
        selected_filters = self.site.competition_league.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.six_hour_time,
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.six_hour_time}".')
        self.verify_events_sorted_by_time()

    def test_005_switch_tab_eg_to_sport_landing_page_or_to_in_play_page(self):
        """
        DESCRIPTION: Switch tab, e.g. to Sport Landing page or to In-Play page
        EXPECTED: Filtering would not be applied to newly selected tab
        """
        self.navigate_to_page(name='sport/cricket')
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        if has_time_filter:
            selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
            self.assertFalse(selected_filters, msg='Time filters selected')
        else:
            self._logger.info(msg='TimeFilters are not available in SLP ')

    def test_006_tapclick_back_into_competitions(self):
        """
        DESCRIPTION: Tap/Click back into Competitions
        EXPECTED: Filtering that previously applied is reset
        """
        self.test_001_clicktap_on_the_competition_tab()

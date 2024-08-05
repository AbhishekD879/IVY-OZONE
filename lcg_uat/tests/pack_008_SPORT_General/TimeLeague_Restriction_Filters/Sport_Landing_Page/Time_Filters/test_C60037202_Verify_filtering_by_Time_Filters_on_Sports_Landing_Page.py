import pytest
from time import sleep
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.time_league_filters
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60037202_Verify_filtering_by_Time_Filters_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60037202
    NAME: Verify filtering by Time Filters on Sports Landing Page
    DESCRIPTION: This Test Case verifies filtering by Time Filters on Sports Landing Page
    PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: Designs for filters:
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
    PRECONDITIONS: **Time Filters are available for Desktop only up to 12 hours and only on Today Tab**
    PRECONDITIONS: 1. Load the app
    """
    keep_browser_open = True

    def verify_event_sort_time(self):
        event_time_list = []
        sections = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(sections) > 0:
            for league in sections:
                if not league.is_expanded():
                    league.expand()
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

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
        PRECONDITIONS: - 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Competitions)
        PRECONDITIONS: - The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours, 2 hours(custom added), 21 hours(custom added)(Sports Pages > Sport Categories > Sport > Competitions)
        PRECONDITIONS: **Designs**
        PRECONDITIONS: Mobile
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
        PRECONDITIONS: Desktop
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
        PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Navigate to Tier 2 Sport Landing page
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=5))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=9))
            self.ob_config.add_football_event_to_england_premier_league(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_football_event_to_england_premier_league(start_time=self.get_date_time_formatted_string(hours=5))
            self.ob_config.add_football_event_to_england_premier_league(start_time=self.get_date_time_formatted_string(hours=9))
            tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.cricket_config.category_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=self.ob_config.cricket_config.category_id)
            tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.football_config.category_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=self.ob_config.football_config.category_id)
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.cricket_config.category_id, enabled=True,
            league_required=False,
            event_filters_values=[1, 3, 6, 12, 24, 48])

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.football_config.category_id, enabled=True,
            league_required=False,
            event_filters_values=[1, 3, 6, 12, 24, 48])

    def test_001_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to Sports Landing page
        EXPECTED: **For Mobile:**
        EXPECTED: * Time Filters Component is displayed with the following time frames: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        EXPECTED: * Filters are not selected or highlighted by default
        EXPECTED: **For Desktop:**
        EXPECTED: * Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        EXPECTED: * Filters are not selected or highlighted by default
        """
        self.site.wait_content_state('HomePage', timeout=10)
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='Cricket', timeout=10)

    def test_002_select_some_time_filter_eg_3_hours(self):
        """
        DESCRIPTION: Select some Time Filter (e.g. 3 hours)
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        sleep(5)
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict['3h'].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], "3h",
                         msg=f'"selected time filter {list(selected_filters.keys())[0]} "'
                             f'does not match expected time filter 3h')
        self.verify_event_sort_time()

    def test_003_for_mobileselect_one_more_filter_eg_24_hoursfor_desktopselect_one_more_filter_eg_12_hours(self):
        """
        DESCRIPTION: **For Mobile:**
        DESCRIPTION: Select one more filter, e.g. 24 hours
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Select one more filter, e.g. 12 hours
        EXPECTED: **For Mobile:**
        EXPECTED: * New selected Time Filter is highlighted and the previous one is removed
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 24 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * New selected Time Filter is highlighted and the previous one is removed
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 12 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict['12h'].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], "12h",
                         msg=f'"selected time filter {list(selected_filters.keys())[0]} "'
                             f'does not match expected time filter 12h')
        self.verify_event_sort_time()

    def test_004_click_on_the_selected_time_filter(self):
        """
        DESCRIPTION: Click on the selected time filter
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict['12h'].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters,
                         msg="Filtering is applied to newly selected tab")

    def test_005_select_filter_with_a_range_where_no_available_events_eg_1_hour(self):
        """
        DESCRIPTION: Select filter with a range where no available events, e.g. 1 hour
        EXPECTED: The message "No events found" is displayed on the current page
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict['1h'].click()
        self.verify_event_sort_time()

    def test_006_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football', timeout=10)
        self.test_002_select_some_time_filter_eg_3_hours()
        self.test_003_for_mobileselect_one_more_filter_eg_24_hoursfor_desktopselect_one_more_filter_eg_12_hours()
        self.test_004_click_on_the_selected_time_filter()
        self.test_005_select_filter_with_a_range_where_no_available_events_eg_1_hour()

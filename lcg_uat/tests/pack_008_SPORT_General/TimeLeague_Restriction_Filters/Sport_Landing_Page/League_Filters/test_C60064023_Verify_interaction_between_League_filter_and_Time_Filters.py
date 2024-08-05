import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.time_league_filters
@pytest.mark.desktop
@vtest
class Test_C60064023_Verify_interaction_between_League_filter_and_Time_Filters(Common):
    """
    TR_ID: C60064023
    NAME: Verify interaction between League filter and Time Filters
    DESCRIPTION: This Test Case verifies interaction between League filter and Time Filters
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

    def verify_selected_filters(self, expected_filters):
        sleep(1.5)
        active_filters = self.timeline_filters.selected_filters
        self.assertEqual(list(active_filters.keys()), expected_filters,
                         msg=f'"selected time filter {list(active_filters.keys())} "'
                             f'does not match expected time filter "{expected_filters}"')

    def verify_event_sort_time(self):
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values()
        if len(sections) > 0:
            for section in sections:
                if not section.is_expanded():
                    section.expand()
                meetings = list(section.items_as_ordered_dict.values())
                self.assertTrue(meetings, msg='No meetings was found on page')
                actual_time_list = []
                for event_data in meetings:
                    if event_data.is_live_now_event:
                        continue
                    else:
                        time = event_data.event_time.split(",")[0]
                        actual_time_list.append(time)
                expected_sort_list = sorted(actual_time_list)
                self.assertEqual(sorted(actual_time_list), expected_sort_list,
                                 msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                     f'Expected text: "{expected_sort_list}"')
        else:
            no_events = self.site.sports_page.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
        PRECONDITIONS: **Time Filters are available for Desktop only up to 12 hours and only on Today Tab**
        PRECONDITIONS: **League Filters are available for Desktop only on Today Tab**
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Navigate to Sports Landing page (Today tab)
        """
        self.cms_config.update_sports_event_filters(tab_name='matches', sport_id=10, enabled=True, top_league_ids='29147',
                                                    test_league_ids='85404', invalid_league_ids='1234', league_enabled=True,
                                                    league_required=True, event_filters_values=[1, 3, 6, 12, 24, 48])
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=4))
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='Cricket')

    def test_001_select_some_time_filter_eg_3_hours(self):
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
        self.__class__.timeline_filters = self.site.cricket.tab_content.timeline_filters
        self.__class__.leagues_and_times = self.timeline_filters.items_as_ordered_dict
        self.__class__.one_hour = self.leagues_and_times.get('1h')
        self.one_hour.click()
        self.verify_selected_filters(expected_filters=['1h'])
        self.verify_event_sort_time()

    def test_002_select_some_league_filter_eg_top_leagues(self):
        """
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
        top_leagues = self.leagues_and_times.get('Top Leagues')
        top_leagues.click()
        self.verify_selected_filters(expected_filters=['Top Leagues', '1h'])
        self.verify_event_sort_time()

    def test_003_click_the_selected_time_filter(self):
        """
        DESCRIPTION: Click the Selected Time Filter
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only that in line with 'Top Leagues' League Filter for that given Sport without time filtering
        EXPECTED: * Events are sorted by Start Time
        """
        self.one_hour.click()
        self.verify_selected_filters(expected_filters=['Top Leagues'])
        self.verify_event_sort_time()

    def test_004_select_another_league_filter_eg_test_league(self):
        """
        DESCRIPTION: Select another League Filter (e.g. 'Test League')
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only that in line with 'Test Leagues' League Filter for that given Sport without time filtering
        EXPECTED: * Events are sorted by Start Time
        """
        test_leagues = self.leagues_and_times.get('Test Leagues')
        test_leagues.click()
        self.verify_selected_filters(expected_filters=['Test Leagues'])
        self.verify_event_sort_time()

    def test_005_select_some_time_filter_eg_12_hours(self):
        """
        DESCRIPTION: Select some Time Filter (e.g. 12 hours)
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 12 hours AND that in line with 'Test Leagues' League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 12 hours AND that in line with 'Test Leagues' League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.__class__.three_hour = self.leagues_and_times.get('3h')
        self.three_hour.click()
        self.verify_selected_filters(expected_filters=['Test Leagues', '3h'])
        self.verify_event_sort_time()

    def test_006_select_another_league_filter_eg_invalid_league(self):
        """
        DESCRIPTION: Select another League Filter (e.g. 'Invalid League')
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        invalid_leagues = self.leagues_and_times.get('Invalid Leagues')
        invalid_leagues.click()
        self.verify_selected_filters(expected_filters=['Invalid Leagues', '3h'])
        self.verify_event_sort_time()

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Any League Filter is not highlighted
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads with all events
        EXPECTED: * Events are sorted by Start Time
        """
        self.device.refresh_page()
        self.__class__.timeline_filters = self.site.cricket.tab_content.timeline_filters
        self.__class__.leagues_and_times = self.timeline_filters.items_as_ordered_dict
        active_filters = self.timeline_filters.selected_filters
        self.assertFalse(active_filters, msg='Filters are selected even after page refresh')
        self.verify_event_sort_time()

    def test_008_select_some_time_filter_where_events_from_selected_time_frame_arent_available_eg_1_hoursselect_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some Time Filter where events from selected time frame aren't available (e.g. 1 hours)
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        self.leagues_and_times.get('1h').click()
        self.verify_selected_filters(expected_filters=['1h'])
        self.verify_event_sort_time()

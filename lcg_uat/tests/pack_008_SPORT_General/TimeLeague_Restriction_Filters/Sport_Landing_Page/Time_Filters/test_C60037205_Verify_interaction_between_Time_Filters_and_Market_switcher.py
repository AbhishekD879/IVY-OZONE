import pytest
import datetime
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.time_league_filters
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60037205_Verify_interaction_between_Time_Filters_and_Market_switcher(Common):
    """
    TR_ID: C60037205
    NAME: Verify interaction between Time Filters and Market switcher
    DESCRIPTION: This Test Case verifies interaction between Time Filters and Market switcher
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
    PRECONDITIONS: 2. Navigate to Sports Landing page (Today tab)
    """
    keep_browser_open = True
    event_markets = [
        ('handicap_2_way',),
        ('total_match_points',)]
    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.rugby_handicap,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.total_points]

    def verify_event_sort_time(self, selected_filter=None):
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        for section in sections:
            meetings = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
                section).items_as_ordered_dict.values())
            self.assertTrue(meetings, msg='No meetings was found on page')
            actual_time_list = []
            for event_data in meetings:
                if event_data.is_live_now_event:
                    continue
                else:
                    split_char = "," if self.brand == "bma" else " "
                    time = event_data.event_time.split(split_char)[0]
                    mon = datetime.datetime.now().strftime("%d %b")
                    append_year = mon + "," + str(datetime.datetime.now().year) + " " + time
                    event_time = datetime.datetime.strptime(append_year, '%d %b,%Y %H:%M').strftime('%Y-%m-%d %H:%M')
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    diff_sec = (datetime.datetime.strptime(event_time, "%Y-%m-%d %H:%M") - datetime.datetime.strptime(
                        current_time, "%Y-%m-%d %H:%M")).seconds
                    if selected_filter:
                        selected_filter_seconds = int(selected_filter) * 60 * 60
                        self.assertLessEqual(diff_sec, selected_filter_seconds,
                                             msg=f'"the displayed events "{diff_sec}" are not less than the selected filter "{selected_filter_seconds}"')
                    actual_time_list.append(time)
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(sorted(actual_time_list), expected_sort_list,
                             msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                 f'Expected text: "{expected_sort_list}"')

    def test_000_preconditions(self):
        tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.rugby_union_config.category_id,
                                                  tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                 sport_id=self.ob_config.rugby_union_config.category_id)
        self.cms_config.update_sports_event_filters(tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    sport_id=self.ob_config.rugby_union_config.category_id, enabled=True,
                                                    league_required=False,
                                                    event_filters_values=[1, 2, 3, 6, 12, 21, 24, 48])
        self.ob_config.add_rugby_union_event_to_rugby_union_all_rugby_union()
        self.ob_config.add_rugby_union_event_to_rugby_union_all_rugby_union(markets=[('handicap_2_way',)])
        self.ob_config.add_rugby_union_event_to_rugby_union_all_rugby_union(markets=[('total_match_points',)],
                                                                            start_time=self.get_date_time_formatted_string(hours=13))

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
        self.site.wait_content_state('HomePage')
        self.navigate_to_page("sport/rugby-union")
        self.site.wait_content_state('rugby-union')
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='filters are not displayed')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(selected_filters, None, msg='Some filters are selected by default but expected to be None')
        filters['3h'].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertIn('3h', selected_filters.keys(), msg='selected filter "3h" is not present in current selected filters')
        self.verify_event_sort_time(selected_filter=3)

    def test_002_select_another_market_from_the_market_switcher(self):
        """
        DESCRIPTION: Select another Market from the Market Switcher
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Rugby Union')
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[1]).click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertIn('3h', selected_filters.keys(),
                      msg='selected filter "3h" is not present in current selected filters')

    def test_003_change_market_from_market_selector_where_no_events_present_or_events_from_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change market from Market Selector, where no events present or events from selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[2]).click()
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), self.expected_list[2].upper(),
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{self.expected_list[2].upper()}"')
        label = self.site.sports_page.tab_content.has_no_events_label()
        self.assertTrue(label, msg='No events available message is not shwon on the page')

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Default Market is displayed in the Market Switcher
        EXPECTED: * Any Time Filter is not highlighted
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
        sleep(5)
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[1]).click()
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), self.expected_list[1].upper(),
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{self.expected_list[1].upper()}"')
        self.verify_event_sort_time()

    def test_006_select_some_time_filter_eg_12_hours(self):
        """
        DESCRIPTION: Select some Time Filter, e.g. 12 hours
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict.get("12h").click()
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[1]).click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertIn('12h', selected_filters.keys(),
                      msg='selected filter "12h" is not present in current selected filters')
        self.verify_event_sort_time(12)

    def test_007_change_time_filter_where_events_from_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change Time Filter, where events from selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        self.test_003_change_market_from_market_selector_where_no_events_present_or_events_from_selected_time_frame_arent_available()

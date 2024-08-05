import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.time_league_filters
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60037204_Verify_filtering_by_Time_Filters_during_switching_tabs_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60037204
    NAME: Verify filtering by Time Filters during switching tabs on Sports Landing Page
    DESCRIPTION: This Test Case verifies filtering by Time Filters during switching tabs on Sports Landing Page
    """
    keep_browser_open = True

    def verify_events_are_sorted_by_time(self):
        """
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
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
        matches_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches
        self.cms_config.update_sports_event_filters(tab_name=matches_tab, sport_id=16, enabled=True,
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
        self.site.wait_content_state('HomePage')
        self.navigate_to_page(name='sport/football')
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='filters are not displayed')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(selected_filters, None, msg='Some filters are selected by default but expected to be None')

    def test_002_select_some_time_filter_eg_3_hours(self, tfilter="12h"):
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
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict[tfilter].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], tfilter,
                         msg=f'"selected time filter {list(selected_filters.keys())[0]} "'
                             f'does not match expected time filter {tfilter}')
        self.verify_events_are_sorted_by_time()
        selected_color = self.site.sports_page.tab_content.timeline_filters.selected_filter.background_color_value
        self.assertEqual(selected_color, vec.colors.SHOW_INFO_COLOR,
                         msg=f'Time Filter actual color "{selected_color}"'
                             f' is not highlighted in blue as expected color '
                             f'"{vec.colors.SHOW_INFO_COLOR}"')

    def test_003_switch_to_another_tab_eg_in_play(self):
        """
        DESCRIPTION: Switch to another tab (e.g. In-Play)
        EXPECTED: * Time Filters Component is not displayed on the In-Play tab
        EXPECTED: * All In-Play Events are displayed without filtering by Time Filter
        """
        self.site.football.tabs_menu.click_button('IN-PLAY')
        self.assertEqual(self.site.football.tabs_menu.current, 'IN-PLAY', msg='In-Play tab is not active')
        self.assertFalse(self.site.sports_page.tab_content.has_timeline_filters())

    def test_004_switch_back_to_matches_tab(self):
        """
        DESCRIPTION: Switch back to Matches tab
        EXPECTED: * Time Filters Component is displayed with the following time frames: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        EXPECTED: * Filters are not selected or highlighted by default
        EXPECTED: * All Events are displayed without filtering by Time Filter
        """
        self.site.football.tabs_menu.click_button('MATCHES')
        self.assertEqual(self.site.football.tabs_menu.current, 'MATCHES', msg='MATCHES tab is not active')
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='filters are not displayed')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(selected_filters, None, msg='Some filters are selected by default but expected to be None')

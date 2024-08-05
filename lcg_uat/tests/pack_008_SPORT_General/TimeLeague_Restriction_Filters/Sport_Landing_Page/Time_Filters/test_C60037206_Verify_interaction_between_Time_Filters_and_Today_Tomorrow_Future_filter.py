import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.time_league_filters
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60037206_Verify_interaction_between_Time_Filters_and_Today_Tomorrow_Future_filter(Common):
    """
    TR_ID: C60037206
    NAME: Verify interaction between Time Filters and Today/Tomorrow/Future filter
    DESCRIPTION: This Test Case verifies interaction between Time Filters and Today/Tomorrow/Future filter
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    time_filters = ['1h', '3h', '6h', '12h', '24h', '48h']

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
        self.cms_config.update_sports_event_filters(tab_name='matches', sport_id=10, enabled=True,
                                                    event_filters_values=[1, 3, 6, 12, 24, 48])
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=5))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(days=1))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(days=2))
        self.site.wait_content_state('HomePage')
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state('Cricket')
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                         msg=f'Actual tab: "{current_tab}" is not same as Expected Tab: "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')

    def test_001_navigate_to_sports_landing_page_today_tab(self):
        """
        DESCRIPTION: Navigate to Sports Landing page (Today Tab)
        EXPECTED: * Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        EXPECTED: * Filters are not selected or highlighted by default
        """
        current_date_tab = self.site.sports_page.date_tab.current_date_tab
        self.assertEqual(current_date_tab, vec.sb.SPORT_DAY_TABS.today,
                         msg=f'Actual tab: "{current_date_tab}" is not same as Expected Tab: "{vec.sb.SPORT_DAY_TABS.today}"')
        flag = self.site.sports_page.tab_content.has_no_events_label()
        if flag:
            raise SiteServeException('There are no available events')

        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        self.assertTrue(has_time_filter, msg='Time filter not available')
        actual_time_filters = self.site.sports_page.tab_content.timeline_filters.items_names
        self.assertTrue(set(self.time_filters).issubset(set(actual_time_filters)), msg=f'Expected Time filters: "{self.time_filters}" are not displayed on UI')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg='Time filters selected')

    def test_002_switch_to_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to Tomorrow Tab
        EXPECTED: * Time Filters Component is not displayed
        """
        self.site.sports_page.date_tab.tomorrow.click()
        self.site.wait_content_state_changed(timeout=5)
        flag = self.site.sports_page.tab_content.has_no_events_label()
        if flag:
            raise SiteServeException('There are no available events')
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        self.assertFalse(has_time_filter, msg='Time filter are available on tomorrow tab')

    def test_003_switch_back_to_today_tab_and_select_some_time_filter_eg_3h(self):
        """
        DESCRIPTION: Switch back to Today Tab and Select some Time filter (e.g. 3h)
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.site.sports_page.date_tab.today.click()
        self.site.wait_content_state_changed(timeout=5)
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        three_hours = filters.get(self.time_filters[1])
        three_hours.click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.time_filters[1],
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.time_filters[1]}".')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='sections and events not available')

    def test_004_switch_to_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to Tomorrow Tab
        EXPECTED: * Time Filters Component is not displayed
        EXPECTED: * Page loads all Tomorrow Events
        """
        self.test_002_switch_to_tomorrow_tab()
        tomorrow_events = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(tomorrow_events, msg='Tomorrow events are not displayed under tomorrow tab')

    def test_005_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to Today Tab
        EXPECTED: * Filters are not selected or highlighted
        EXPECTED: * Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        """
        self.site.sports_page.date_tab.today.click()
        self.site.wait_content_state_changed(timeout=5)
        self.test_001_navigate_to_sports_landing_page_today_tab()

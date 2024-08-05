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
@pytest.mark.time_league_filters_negative
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.reg167_fix
@vtest
class Test_C60063708_Verify_filtering_by_Time_Filters_for_Tier_2_Sports_without_Market_Selector_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60063708
    NAME: Verify filtering by Time Filters for Tier 2 Sports without Market Selector  on Sports Landing Page
    DESCRIPTION: This test case verifies filtering by Time Filters for Tier 2 Sports without Market Selector  on Sports Landing Page
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
    PRECONDITIONS: 2. Navigate to Sports Landing page (market selector should be absent for this sport), e.g. Cricket
    """
    keep_browser_open = True
    three_hours, six_hours = '3h', '6h'

    def test_000_preconditions(self):
        """
        Description : Checking whether sport "cricket" is enabled or disable
        """
        self.cms_config.update_sports_event_filters(tab_name='matches', sport_id=10, enabled=True,
                                                    event_filters_values=[1, 3, 6, 12, 24, 48])
        if tests.settings.backend_env != 'prod':
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket',
                                                                                              status=False)
            self.assertFalse(market_switcher_status, msg='Market switcher is enabled for Snooker sport')

            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=5))

        self.site.wait_content_state('HomePage')
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state('Cricket')
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                         msg=f'Actual tab: "{current_tab}" is not same as Expected Tab: "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')

    def test_001_select_filter_eg_3_hour(self):
        """
        DESCRIPTION: Select filter, e.g. 3 hour
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        flag = self.site.sports_page.tab_content.has_no_events_label()
        if flag:
            raise SiteServeException('There are no available events')
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        three_hours = filters.get(self.three_hours)
        three_hours.click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.three_hours,
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.three_hours}".')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        if sections:
            self.assertTrue(sections, msg='sections and events not available')
        else:
            self.assertTrue(self.site.contents.tab_content.has_no_events_label(),
                            msg="'No Events Found' label was not displayed")

    def test_002_click_on_the_selected_time_filter(self):
        """
        DESCRIPTION: Click on the selected time filter
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        three_hours = filters.get(self.three_hours)
        three_hours.click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg='Time filters selected')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        if sections:
            self.assertTrue(sections, msg='sections and events not available')
        else:
            self.assertTrue(self.site.contents.tab_content.has_no_events_label(),
                            msg="'No Events Found' label was not displayed")

    def test_003_select_filter_eg_6_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 6 hours
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 6 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 6 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        three_hours = filters.get(self.six_hours)
        three_hours.click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.six_hours,
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.six_hours}".')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        if sections:
            self.assertTrue(sections, msg='sections and events not available')
        else:
            self.assertTrue(self.site.contents.tab_content.has_no_events_label(),
                            msg="'No Events Found' label was not displayed")

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        self.device.refresh_page()
        self.site.wait_content_state('Cricket')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg='Time filters selected')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        if sections:
            self.assertTrue(sections, msg='sections and events not available')
        else:
            self.assertTrue(self.site.contents.tab_content.has_no_events_label(),
                            msg="'No Events Found' label was not displayed")

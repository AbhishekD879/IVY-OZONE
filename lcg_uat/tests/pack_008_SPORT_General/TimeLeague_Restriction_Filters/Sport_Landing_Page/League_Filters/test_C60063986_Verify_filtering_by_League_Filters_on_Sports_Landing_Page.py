import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.time_league_filters
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C60063986_Verify_filtering_by_League_Filters_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60063986
    NAME: Verify filtering by League Filters on Sports Landing Page
    DESCRIPTION: This Test Case verifies filtering by League Filters on Sports Landing Page
    """
    keep_browser_open = True

    def verify_events_sorted_by_time(self, selected_filter=True):
        event_time_list = []
        sections = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        if selected_filter:
            if len(sections) > 0:
                for league in sections:
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
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.cricket_config.category_id)[0]
        type_id = event['event']['typeId']
        # The conditions is returning true if the sporteventfilter is on in structure but test case
        # need to verify both the top leauge and time filter if they and not configured it won't show
        if not self.cms_config.get_system_configuration_structure().get('FeatureToggle', {})['SportEventFilters']:
            raise CmsClientException('In FeatureToggle SportEventFilters is disabled in CMS')
        self.cms_config.update_sports_event_filters(
                tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                sport_id=self.ob_config.cricket_config.category_id,
                top_league_ids=type_id,
                test_league_ids=type_id,
                invalid_league_ids='1234',
                league_enabled=True,
                enabled=True,
                league_required=True,
                event_filters_values=[1, 3, 6, 12, 24, 48])

    def test_001_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to Sports Landing page
        EXPECTED: * League Filters Component is displayed with the following filters: 'Top Leagues', 'Test League', 'Invalid League'
        EXPECTED: * Filters are not selected or highlighted by default
        """
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

    def test_002_select_some_league_filter_eg_top_leagues(self):
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

    def test_003_select_one_more_filter_eg_test_league(self):
        """
        DESCRIPTION: Select one more filter, e.g. 'Test League'
        EXPECTED: * New selected League Filter is highlighted and the previous one is removed
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.assertIn(vec.bma.TEST_LEAGUE, self.filter_name, msg=f'"{vec.bma.TEST_LEAGUE}" not contain '
                                                                 f'"{self.filter_name}"')
        self.filter[1].click()
        selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
        self.assertIn(self.filter_name[1], selected_filters,
                      msg=f'Actual "{self.filter_name[1]}" is not same as expected "{selected_filters}"')
        self.assertNotIn(self.filter_name[0], selected_filters, msg=f'Actual "{self.filter_name[0]}"'
                                                                    f' is present "{selected_filters}"')
        self.verify_events_sorted_by_time()

    def test_004_click_on_the_selected_test_league_filter(self):
        """
        DESCRIPTION: Click on the selected 'Test League' filter
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        self.filter[1].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg=f'Filters are selected or highlighted by default')
        self.verify_events_sorted_by_time(selected_filter=False)

    def test_005_select_filter_with_a_range_where_no_available_events_eg_invalid_league(self):
        """
        DESCRIPTION: Select filter with a range where no available events, e.g. 'Invalid League'
        EXPECTED: * Selected League Filter is highlighted
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

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg=f'Filters are selected or highlighted by default')
        self.verify_events_sorted_by_time(selected_filter=False)
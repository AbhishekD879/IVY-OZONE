import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.time_league_filters
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60035089_Verify_Filtering_options_Removing_Highlighted_filter_for_Tier_2_sports(Common):
    """
    TR_ID: C60035089
    NAME: Verify Filtering options,  Removing Highlighted filter  for Tier 2 sports
    DESCRIPTION: This test case verifies Filtering options, Removing Highlighted filter for Tier 2 sports
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
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
    keep_browser_open = True

    def verify_event_sort_time(self):
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        if len(sections) > 0:
            for section in sections:
                meetings = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.get(
                    section).items_as_ordered_dict.values())
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
            tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.cricket_config.category_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=self.ob_config.cricket_config.category_id)
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            sport_id=self.ob_config.cricket_config.category_id, enabled=True,
            league_required=False,
            event_filters_values=[1, 3, 6, 12, 24, 48])
        self.site.wait_content_state('HomePage', timeout=10)
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='Cricket')

    def test_001_clicktap_on_the_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on the 'Competition' tab
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.cricket_config.category_id)
        self.site.competition_league.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab = self.site.competition_league.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_002_select_filter_eg_3_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 3 hours
        EXPECTED: - Page loads only events that are due to start within the next 3 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict['3h'].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], "3h",
                         msg=f'"selected time filter {list(selected_filters.keys())[0]} "'
                             f'does not match expected time filter 3h')
        self.verify_event_sort_time()

    def test_003_select_one_more_filter_eg_24_hours(self):
        """
        DESCRIPTION: Select one more filter, e.g. 24 hours
        EXPECTED: - New Time Filter is highlighted and the previous one is removed
        EXPECTED: - Page loads only events that are due to start within the next 24 hours for that given league
        EXPECTED: - Events are sorted by time
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict['12h'].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], "12h",
                         msg=f'"selected time filter {list(selected_filters.keys())[0]} "'
                             f'does not match expected time filter 12h')
        self.verify_event_sort_time()

    def test_004_click_on_the_selected_time_filter_to_remove_highlight(self):
        """
        DESCRIPTION: Click on the selected time filter to remove highlight
        EXPECTED: User returns to default view
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict['12h'].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters,
                         msg="Filtering is applied to newly selected tab")

    def test_005_select_filter_with_a_range_where_no_available_events_eg_1_hour(self):
        """
        DESCRIPTION: Select filter with a range where no available events, e.g. 1 hour
        EXPECTED: The message "No events found" is displayed on current page
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict['1h'].click()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], "1h",
                         msg=f'"selected time filter {list(selected_filters.keys())[0]} "'
                             f'does not match expected time filter 1h')
        self.verify_event_sort_time()

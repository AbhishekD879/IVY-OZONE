import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.reg165_fix
@pytest.mark.sports
@pytest.mark.time_league_filiters
@vtest
class Test_C60035090_Verify_Time_Filters_during_switching_tabs_for_Tier_2_sports(Common):
    """
    TR_ID: C60035090
    NAME: Verify Time Filters during switching tabs for Tier 2 sports
    DESCRIPTION: This test case verifies Time Filters during switching tabs for Tier 2 sports
    """
    keep_browser_open = True
    three_hour_time = '3h'
    six_hour_time = '6h'

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Competitions)
        PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Competitions)
        PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
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
        self.cms_config.update_sports_event_filters(tab_name='competitions', sport_id=10, enabled=True,
                                                    event_filters_values=[1, 3, 6, 12, 24, 48])
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=5))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=9))
        self.site.wait_content_state('HomePage')
        self.navigate_to_page(name='sport/cricket')

    def test_001_clicktap_on_the_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on the 'Competition' tab
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        competitions_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                        10)
        self.site.contents.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.contents.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
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
        three_hours = self.filters.get(self.three_hour_time)
        three_hours.click()
        selected_filters = self.site.competition_league.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.three_hour_time,
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.three_hour_time}".')
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        if not sections:
            no_events_found_status = self.site.competition_league.tab_content.has_no_events_label
            self.assertTrue(no_events_found_status, msg='when there are no events, no events label is not appeared')

    def test_003_switch_tab_eg_to_sport_landing_page_or_to_in_play_page(self):
        """
        DESCRIPTION: Switch tab, e.g. to Sport Landing page or to In-Play page
        EXPECTED: Filtering would not be applied to newly selected tab
        """
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state_changed(timeout=10)

    def test_004_tapclick_back_into_competitions(self):
        """
        DESCRIPTION: Tap/Click back into Competitions
        EXPECTED: Filtering that previously applied is reset
        """
        competitions_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                        10)
        self.site.contents.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.contents.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED:
        """
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        six_hours = self.filters.get(self.six_hour_time)
        six_hours.click()
        selected_filters = self.site.competition_league.tab_content.timeline_filters.selected_filters
        self.assertEqual(list(selected_filters.keys())[0], self.six_hour_time,
                         msg=f'Actual time filter: "{list(selected_filters.keys())[0]}" is not same as'
                             f'Expected time filter: "{self.six_hour_time}".')
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        if not sections:
            no_events_found_status = self.site.competition_league.tab_content.has_no_events_label
            self.assertTrue(no_events_found_status,
                            msg='when there are no events, no events label is not appeared')

    def test_006_navigate_to_other_sport__competitions_tab(self):
        """
        DESCRIPTION: Navigate to other sport > competitions tab
        EXPECTED: Filtering would not be applied to currently selected tab
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

    def test_007_return_to_tab_from_step_1(self):
        """
        DESCRIPTION: Return to tab from step 1
        EXPECTED: Filtering that previously applied is reset
        """
        self.navigate_to_page(name='sport/cricket')
        competitions_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                        10)
        self.site.contents.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.contents.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        self.assertTrue(has_time_filter, msg='Time filter not available')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg='Time filters selected')

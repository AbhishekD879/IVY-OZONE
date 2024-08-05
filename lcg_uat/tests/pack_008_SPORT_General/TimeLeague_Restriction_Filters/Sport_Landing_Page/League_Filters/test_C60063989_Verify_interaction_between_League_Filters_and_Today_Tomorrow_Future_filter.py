import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.time_league_filters
@vtest
class Test_C60063989_Verify_interaction_between_League_Filters_and_Today_Tomorrow_Future_filter(Common):
    """
    TR_ID: C60063989
    NAME: Verify interaction between League Filters and Today/Tomorrow/Future filter
    DESCRIPTION: This Test Case verifies interaction between League Filters and Today/Tomorrow/Future filter
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
    keep_browser_open = True
    device_name = tests.desktop_default
    added_filters = None

    def verify_event_sort_time(self):
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        for section in sections:
            meetings = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(
                section).items_as_ordered_dict.values())
            self.assertTrue(meetings, msg='No meetings was found on page')
            actual_time_list = []
            for event_data in meetings:
                if event_data.is_live_now_event:
                    continue
                else:
                    split_char = "," if self.brand == "bma" else " "
                    time = event_data.event_time.split(split_char)[0]
                    actual_time_list.append(time)
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(sorted(actual_time_list), expected_sort_list,
                             msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                 f'Expected text: "{expected_sort_list}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages > Sport Categories > Sport > Matches)
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            type_id = event['event']['typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            type_id = event.ss_response['event']['typeId']

        sport_event_filters_enable = self.cms_config.get_system_configuration_structure()['FeatureToggle'][
            'SportEventFilters']
        if not sport_event_filters_enable:
            self.cms_config.update_system_configuration_structure(config_item='Feature Toggle',
                                                                  field_name='SportEventFilters',
                                                                  field_value=True)
        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.football_config.category_id,
            top_league_ids=type_id,
            test_league_ids=type_id,
            invalid_league_ids='1234',
            league_enabled=True,
            enabled=True,
            league_required=True,
            event_filters_values=[1, 2, 6, 12, 24, 48])

        filters = self.cms_config.get_sports_tab_data(sport_id=self.ob_config.football_config.category_id, tab_name='matches').get('filters')
        time_filters = [f'{f}h' for f in filters.get('time').get('values')]
        league_filters = [f.get('leagueName') for f in filters.get('league').get('values')]
        self.__class__.added_filters = league_filters + time_filters

        self.site.wait_content_state('HomePage')

    def test_001_navigate_to_sports_landing_page_today_tab(self):
        """
        DESCRIPTION: Navigate to Sports Landing page (Today Tab)
        EXPECTED: * League Filters Component is displayed with the following filters: 'Top Leagues', 'Test League', 'Invalid League'
        EXPECTED: * Filters are not selected or highlighted by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                     self.ob_config.football_config.category_id)
        active_tab = self.site.contents.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Matches tab is not active, active is "{active_tab}"')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg=f'Filters are selected or highlighted by default')
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        for filter_name, filter_loc in self.filters.items():
            self.assertIn(filter_name, self.added_filters, msg=f'"Filter {filter_name} is not added {self.added_filters}"')

    def test_002_switch_to_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to Tomorrow Tab
        EXPECTED: * League Filters Component is not displayed
        """
        self.site.football.date_tab.tomorrow.click()
        self.assertEqual(self.site.football.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.tomorrow,
                         msg=f'Current active tab: "{self.site.football.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.tomorrow}"')
        self.assertFalse(self.site.sports_page.tab_content.has_timeline_filters(expected_result=False),
                         msg="League Filters are displayed")

    def test_003_switch_back_to_today_tab_and_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Switch back to Today Tab and Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.site.football.date_tab.today.click()
        self.assertEqual(self.site.football.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.today,
                         msg=f'Current active tab: "{self.site.football.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.today}"')
        self.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        filter_name = list(self.filters.keys())
        self.assertIn(vec.bma.TOP_LEAGUE, filter_name, msg=f'"{vec.bma.TOP_LEAGUE}" not contain '
                                                           f'"{filter_name}"')
        self.filters.get("Top Leagues").click()
        selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
        self.assertIn("Top Leagues", selected_filters, msg=f'Actual "{vec.bma.TOP_LEAGUE}"'
                                                           f' is not same as expected "{selected_filters}"')
        self.verify_event_sort_time()

    def test_004_switch_to_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to Tomorrow Tab
        EXPECTED: * League Filters Component is not displayed
        EXPECTED: * Page loads all Tomorrow Events
        """
        self.test_002_switch_to_tomorrow_tab()
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        if len(sections) == 0:
            no_events = self.site.football.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')
        else:
            self.assertTrue(sections, msg='No sections found in Tomorrow tab')

    def test_005_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to Today Tab
        EXPECTED: * Filters are not selected or highlighted
        EXPECTED: * League Filters Component is displayed with the following filters: 'Top Leagues', 'Test League', 'Invalid League'
        """
        self.site.football.date_tab.today.click()
        self.assertEqual(self.site.football.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.today,
                         msg=f'Current active tab: "{self.site.football.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.today}"')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters, msg=f'Filters are selected or highlighted by default')
        for filter_name, filter_loc in self.filters.items():
            self.assertIn(filter_name, self.added_filters, msg=f'"Filter {filter_name} is not added {self.added_filters}"')

import pytest
import tests
import datetime
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest
from crlat_siteserve_client.utils.exceptions import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.time_league_filters
@vtest
class Test_C60035081_Verify_Filtering_options_Removing_Highlighted_filter_for_Tier_1_sports(Common):
    """
    TR_ID: C60035081
    NAME: Verify Filtering options, Removing Highlighted filter for Tier 1 sports
    DESCRIPTION: This test case verifies Filtering options,  Removing Highlighted filter for Tier 1 sports
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
    PRECONDITIONS: 2. Navigate to Tier 1 Sport Landing page
    PRECONDITIONS: 3. Click/Tap on the 'Competition' tab
    """
    keep_browser_open = True
    added_filters = ['1h', '2h', '3h', '6h', '12h', '21h', '24h', '48h']

    def verify_event_sort_time(self, selected_filter):
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        for section in sections:
            meetings = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.get(
                section).items_as_ordered_dict.values())
            self.assertTrue(meetings, msg='No meetings was found on page')
            actual_time_list = []
            for event_data in meetings:
                if event_data.is_live_now_event:
                    continue
                else:
                    split_char = "," if self.brand == "bma" else " "
                    time = event_data.event_time.split(split_char)[0]
                    mon = datetime.datetime.now().strftime("%d %b") if section.upper() == "TODAY" else section
                    if section.upper() == "TOMORROW":
                        mon = event_data.event_time.split(split_char, 1)[1].strip()
                    append_year = mon + "," + str(datetime.datetime.now().year) + " " + time
                    event_time = datetime.datetime.strptime(append_year, '%d %b,%Y %H:%M').strftime('%Y-%m-%d %H:%M')
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    diff_sec = (datetime.datetime.strptime(event_time, "%Y-%m-%d %H:%M") - datetime.datetime.strptime(
                        current_time, "%Y-%m-%d %H:%M")).seconds
                    selected_filter_seconds = int(selected_filter) * 60 * 60
                    self.assertLessEqual(diff_sec, selected_filter_seconds,
                                         msg=f'"the displayed events "{diff_sec}" are not less than the selected filter "{selected_filter_seconds}"')
                    actual_time_list.append(time)
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(sorted(actual_time_list), expected_sort_list,
                             msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                 f'Expected text: "{expected_sort_list}"')

    def test_000_preconditions(self):
        tennis_category_id = self.ob_config.backend.ti.tennis.category_id
        if tests.settings.backend_env != 'prod':
            self.check_sport_configured(tennis_category_id)
            self.__class__.event1 = self.ob_config.add_tennis_event_to_davis_cup(
                start_time=self.get_date_time_formatted_string(hours=1))
            self.ob_config.add_tennis_outright_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(hours=1))
            self.ob_config.add_tennis_event_enhanced_multiples(start_time=self.get_date_time_formatted_string(hours=1))
            self.ob_config.add_tennis_event_to_nice_open(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_tennis_event_to_davis_cup(start_time=self.get_date_time_formatted_string(hours=5))
            self.ob_config.add_tennis_event_to_davis_cup(start_time=self.get_date_time_formatted_string(hours=3))
            sport_event_filters_enable = self.cms_config.get_system_configuration_structure()['FeatureToggle'][
                'SportEventFilters']
            if not sport_event_filters_enable:
                self.cms_config.update_system_configuration_structure(config_item='Feature Toggle',
                                                                      field_name='SportEventFilters',
                                                                      field_value=True)
            tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.tennis_config.category_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=self.ob_config.tennis_config.category_id)
        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            sport_id=self.ob_config.tennis_config.category_id, enabled=True,
            league_required=False,
            event_filters_values=[1, 2, 3, 6, 12, 21, 24, 48])

        self.site.wait_content_state('HomePage')
        self.site.open_sport(name='TENNIS', timeout=30)
        try:
            self.site.tennis.tabs_menu.items_as_ordered_dict.get(
                vec.sb.SPORT_TABS_INTERNAL_NAMES.competitions.upper()).is_displayed()
        except Exception:
            raise SiteServeException('Competitions tab is not found under Tennis')
        self.site.tennis.tabs_menu.click_button(vec.sb.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
        current_tab = self.site.tennis.tabs_menu.current
        expected_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()
        self.assertEqual(current_tab, expected_tab,
                         msg=f'Active tab is "{current_tab}" but "{expected_tab}" is expected to be active')

    def test_001_clicktap_on_some_league(self):
        """
        DESCRIPTION: Click/Tap on some League
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        leagues = self.site.tennis.tab_content
        self.assertTrue(leagues, msg=f'Competitions page does not have any section')
        if tests.settings.backend_env != 'prod':
            section_name_list = self.event1.ss_response["event"]["typeName"]
            if self.device_type == 'desktop':
                league = leagues.items_as_ordered_dict.get(section_name_list)
            else:
                league = leagues.competitions_categories.items_as_ordered_dict.get(section_name_list)
        else:
            if self.device_type == 'desktop':
                accordions = leagues.items_as_ordered_dict
                league_name = next((league_name for league_name in accordions if
                                    ("SINGLES" not in league_name.upper() and "OPEN" not in league_name.upper())),
                                   list(accordions.keys())[0])
                league = accordions.get(league_name)
            else:
                accordions = leagues.competitions_categories.items_as_ordered_dict
                league_name = next((league_name for league_name in accordions if ("SINGLES" not in league_name.upper() and "OPEN" not in league_name.upper())),list(accordions.keys())[0])
                league = accordions.get(league_name)
            section_name_list = league.event_name
        self.assertTrue(league, msg=f'Cannot find "{section_name_list}" section on Competitions page')
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')
        selected_filters = self.site.tennis.tab_content.timeline_filters.selected_filters
        self.assertIsNone(selected_filters, msg="Filter is already selected")
        filters = self.site.tennis.tab_content.timeline_filters.items_as_ordered_dict
        for filter_name, filter_loc in filters.items():
            self.assertIn(filter_name, self.added_filters, msg="Filter is not added")

    def test_002_select_filter_eg_3_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 3 hours
        EXPECTED: - Page loads only events that are due to start within the next 3 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        self.__class__.selected_filter = 3
        self.site.tennis.tab_content.timeline_filters.items_as_ordered_dict.get("3h").click()
        selected_filters = self.site.tennis.tab_content.timeline_filters.selected_filters
        self.assertEqual("3h", list(selected_filters.keys())[0], msg="3h Filter is not selected")
        self.verify_event_sort_time(self.selected_filter)

    def test_003_select_one_more_filter_eg_24_hours(self):
        """
        DESCRIPTION: Select one more filter, e.g. 24 hours
        EXPECTED: - New Time Filter is highlighted and the previous one is removed
        EXPECTED: - Page loads only events that are due to start within the next 24 hours for that given league
        EXPECTED: - Events are sorted by time
        """
        self.selected_filter = 1
        self.site.tennis.tab_content.timeline_filters.items_as_ordered_dict.get("1h").click()
        selected_filters = self.site.tennis.tab_content.timeline_filters.selected_filters
        self.assertEqual("1h", list(selected_filters.keys())[0], msg="1h Filter is not selected")
        self.verify_event_sort_time(self.selected_filter)

    def test_004_click_on_the_selected_time_filter_to_remove_highlight(self):
        """
        DESCRIPTION: Click on the selected time filter to remove highlight
        EXPECTED: User returns to default view
        """
        self.site.tennis.tab_content.timeline_filters.items_as_ordered_dict.get("1h").click()
        selected_filters = self.site.tennis.tab_content.timeline_filters.selected_filters
        self.assertIsNone(selected_filters, msg="Filter is already selected")

    def test_005_select_filter_with_a_range_where_no_available_events_eg_1_hour(self):
        """
        DESCRIPTION: Select filter with a range where no available events, e.g. 1 hour
        EXPECTED: The message "No events found" is displayed on current page
        """
        sec_tennis = self.site.tennis.tab_content
        self.site.tennis.tab_content.timeline_filters.items_as_ordered_dict.get("1h").click()
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        if len(sections) == 0:
            no_events = sec_tennis.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')
        else:
            for section in sections:
                meetings = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.get(
                    section).items_as_ordered_dict.values())
                if len(meetings) == 0:
                    no_events = sec_tennis.has_no_events_label()
                    self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')
                else:
                    self.assertTrue(meetings, msg='No meetings was found on page')

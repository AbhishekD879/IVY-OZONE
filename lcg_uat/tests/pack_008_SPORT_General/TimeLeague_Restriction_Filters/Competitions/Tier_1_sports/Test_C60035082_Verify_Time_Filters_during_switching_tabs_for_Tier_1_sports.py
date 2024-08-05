import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.time_league_filters
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60035082_Verify_Time_Filters_during_switching_tabs_for_Tier_1_sports(Common):
    """
    TR_ID: C60035082
    NAME: Verify Time Filters during switching tabs for Tier 1 sports
    DESCRIPTION: This test case verifies Time Filters during switching tabs  for Tier 1 sports
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: - 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Competitions)
    PRECONDITIONS: - The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours(Sports Pages > Sport Categories > Sport > Competitions)
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Mobile
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
    PRECONDITIONS: Desktop
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Tier1 Sport Landing page
    PRECONDITIONS: 3. Click/Tap on the 'Competition' tab
    """
    keep_browser_open = True
    markets = [('to_qualify',),
               ('over_under_total_goals', {'over_under': 2.5}),
               ('both_teams_to_score',),
               ('draw_no_bet',),
               ('first_half_result',),
               ('match_result_and_both_teams_to_score',),
               ('next_team_to_score',),
               ('extra_time_result',)]

    def navigate_to_league(self, league_category, league_name):

        if tests.settings.backend_env != 'prod':
            if self.device_type == 'desktop':
                self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[
                    vec.sb_desktop.COMPETITIONS_SPORTS].click()
                competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            else:
                competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(competitions, msg='No competitions are present on page')

        if self.device_type == 'mobile':
            category = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict.get(
                league_category)
        else:
            category = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(league_category)
        self.assertTrue(category, msg='category is not displayed')
        if not category.is_expanded():
            category.expand()
        league = category.items_as_ordered_dict.get(league_name)
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage', timeout=30)

    def verify_events_are_sorted_by_time(self):
        """
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        event_time_list = []
        sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
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

    def test_000_preconditions(self):

        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')
            self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
            self.ob_config.add_football_event_to_england_championship()

            sport_event_filters_enable = self.cms_config.get_system_configuration_structure()['FeatureToggle'][
                'SportEventFilters']

            if not sport_event_filters_enable:
                self.cms_config.update_system_configuration_structure(config_item='Feature Toggle',
                                                                      field_name='SportEventFilters',
                                                                      field_value=True)

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            sport_id=self.ob_config.football_config.category_id,
            enabled=True, event_filters_values=[1, 3, 6, 12, 24, 48])

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.football_config.category_id,
            enabled=True, event_filters_values=[1, 3, 6, 12, 24, 48])

        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='football')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.site.wait_content_state_changed()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

    def test_001_clicktap_on_some_league(self):
        """
        DESCRIPTION: Click/Tap on some League
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        if tests.settings.backend_env != 'prod':
            if self.device_type == 'desktop':
                self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[
                    vec.sb_desktop.COMPETITIONS_SPORTS].click()
                competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            else:
                competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(competitions, msg='No competitions are present on page')

            if self.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = 'Auto Test'
                self.navigate_to_league(league_category=league,
                                        league_name=vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME)
            else:
                league = 'AUTO TEST'
                self.navigate_to_league(league_category=league, league_name=vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME)
        else:
            if self.brand == 'ladbrokes' and self.device_type == 'desktop':
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(),
                                        league_name=vec.siteserve.PREMIER_LEAGUE_NAME)
            else:
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND,
                                        league_name=vec.siteserve.PREMIER_LEAGUE_NAME)

    def test_002_select_filter_eg_12_hours(self, tfilter="12h"):
        """
        DESCRIPTION: Select filter, e.g. 12 hours
        EXPECTED: - Page loads only events that are due to start within the next 12 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
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

    def test_003_switch_tab_eg_to_sport_landing_page_or_to_in_play_page(self):
        """
        DESCRIPTION: Switch tab, e.g. to Sport Landing page or to In-Play page
        EXPECTED: Filtering would not be applied to newly selected tab
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football', timeout=30)
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters,
                         msg="Filtering is applied to newly selected tab")

    def test_004_tapclick_back_into_competitions(self):
        """
        DESCRIPTION: Tap/Click back into Competitions
        EXPECTED: Filtering that previously applied is reset
        """
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.site.wait_content_state_changed()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')
        self.test_001_clicktap_on_some_league()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters,
                         msg="Filtering is applied to newly selected tab")

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED:
        """
        self.test_002_select_filter_eg_12_hours()

    def test_006_navigate_to_other_sport__competitions_tab(self):
        """
        DESCRIPTION: Navigate to other sport > competitions tab
        EXPECTED: Filtering would not be applied to currently selected tab
        """
        self.site.back_button_click()
        if tests.settings.backend_env != 'prod':
            vec.siteserve.ENGLAND = 'ENGLAND'
            if self.brand == 'ladbrokes' and self.device_type == 'desktop':
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(),
                                        league_name=vec.siteserve.CHAMPIONSHIP)
            else:
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND, league_name=vec.siteserve.CHAMPIONSHIP)
        else:
            if self.brand == 'ladbrokes' and self.device_type == 'desktop':
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(),
                                        league_name=vec.siteserve.CHAMPIONSHIP)
            else:
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND, league_name=vec.siteserve.CHAMPIONSHIP)

    def test_007_return_to_tab_from_step_1(self):
        """
        DESCRIPTION: Return to tab from step 1
        EXPECTED: Filtering that previously applied is reset
        """
        self.site.back_button_click()
        self.test_001_clicktap_on_some_league()
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters,
                         msg="Filtering is applied to newly selected tab")

    def test_008_select_filter_eg_6_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 6 hours
        EXPECTED: - Page loads only events that are due to start within the next 6 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        self.test_002_select_filter_eg_12_hours(tfilter="6h")

    def test_009_tap_change_competition_link_and_select_other_league_from_the_list_just_for_mobile(self):
        """
        DESCRIPTION: Tap 'Change competition' link and select other league from the list (just for mobile)
        EXPECTED: Filtering would not be applied to currently selected league
        """
        if self.device_type == 'mobile':
            change_competition_selector = self.site.competition_league.title_section.competition_selector_link.name
            self.assertEqual(change_competition_selector, vec.sb.CHANGE_COMPETITION,
                             msg=f'Competition header with Change Competition selector is not same'
                                 f'Actual: "{change_competition_selector}" '
                                 f'Expected: "{vec.sb.CHANGE_COMPETITION}"')
            self.site.competition_league.title_section.competition_selector_link.click()

            competitions = self.site.competition_league.competition_list.items_as_ordered_dict
            self.assertTrue(competitions, msg='No competitions are present on page')
            self.assertIn(vec.siteserve.ENGLAND, competitions,
                          msg=f'"{vec.siteserve.ENGLAND}" is not present in competitions "{competitions.keys()}"')

            competition = competitions[vec.siteserve.ENGLAND].items_as_ordered_dict[vec.siteserve.CHAMPIONSHIP]
            competition.click()
            selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
            self.assertFalse(selected_filters,
                             msg="Filtering is applied to currently selected league")
            self.site.back_button_click()
            selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
            self.assertFalse(selected_filters,
                             msg="Filtering that previously applied is not reset")

    def test_010_tapclick_back_into_previously_league(self):
        """
        DESCRIPTION: Tap/Click back into previously league
        EXPECTED: Filtering that previously applied is reset
        """
        # Covered in step 9

import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.time_league_filters
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C64055788_League_filter_Time_filter_should_disappear_if_there_is_no_events_available_in_Matches_tab_competitions_tab(Common):
    """
    TR_ID: C64055788
    NAME: League filter & Time filter should disappear if there is no events available in Matches tab & competitions tab.
    DESCRIPTION: Verify that the league filter & time filter should disappear if there is no events available in Matches tab & competitions tab.
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: * Checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; Feature Toggle-&gt;sporteventfilters.
        PRECONDITIONS: * Initially validate for tier-1 sport.
        PRECONDITIONS: Condition 1:-
        PRECONDITIONS: *Any one Time Filter in Matches and Competitions page & League Filter in Matches page should be configured in CMS.
        PRECONDITIONS: *No events should be available in SLP & Competitions page in Front End.
        PRECONDITIONS: Condition 2:-
        PRECONDITIONS: *Create 72h Time Filter  in Matches and Competitions page & any league filter in Matches page should be configured in CMS.
        PRECONDITIONS: *Events should be available beyond 72h in SLP & Competitions page in Front End.
        PRECONDITIONS: Condition 3:-
        PRECONDITIONS: *Configure any Time Filter between 1h-72h & Valid League Filter in CMS.
        PRECONDITIONS: *Events should be available within 72h in SLP & Competitions page in Front End.
        PRECONDITIONS: Condition 4:-
        PRECONDITIONS: *Configure Time Filter from 1h-72h & create invalid League(The league which don't have available events in FE) Filter in CMS.
        PRECONDITIONS: *Events should be available within 72h in SLP & Competitions page in Front End.
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=5))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=9))
            self.ob_config.add_football_event_to_england_premier_league(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_football_event_to_england_premier_league(start_time=self.get_date_time_formatted_string(hours=5))
            self.ob_config.add_football_event_to_england_premier_league(start_time=self.get_date_time_formatted_string(hours=9))

            # Tier 1
            tab_id_matches = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.football_config.category_id,
                                                              tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
            tab_id_competitions = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.football_config.category_id,
                                                                   tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions)

            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id_matches, enabled="true",
                                                     sport_id=self.ob_config.football_config.category_id)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id_competitions, enabled="true",
                                                     sport_id=self.ob_config.football_config.category_id)
        event_1 = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        type_id_1 = event_1['event']['typeId']
        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.football_config.category_id,
            top_league_ids=type_id_1,
            test_league_ids=type_id_1,
            invalid_league_ids='1234',
            league_enabled=True,
            enabled=True,
            league_required=True,
            event_filters_values=[1, 3, 6, 12, 24, 48])

        # Tier 2
        event_2 = self.get_active_events_for_category(category_id=self.ob_config.cricket_config.category_id)[0]
        type_id_2 = event_2['event']['typeId']

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.cricket_config.category_id,
            top_league_ids=type_id_2,
            test_league_ids=type_id_2,
            invalid_league_ids='1234',
            league_enabled=True,
            enabled=True,
            league_required=True,
            event_filters_values=[1, 3, 6, 12, 24, 48])
        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            sport_id=self.ob_config.cricket_config.category_id,
            enabled=True,
            event_filters_values=[1, 3, 6, 12, 24, 48])

    def test_001_based_on_pre_condition_1_navigate_to_sports_landing_page_gt_matches_tab(self):
        """
        DESCRIPTION: Based on Pre-Condition 1 Navigate to Sports Landing Page-&gt; Matches tab.
        EXPECTED: * 'No events Found' message will be displayed.
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
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.__class__.filter = list(self.filters.values())
        self.__class__.filter_name = list(self.filters.keys())
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

    def test_002_based_on_pre_condition_1_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Based on Pre-Condition 1 Navigate to Competitions page.
        EXPECTED: * 'No events Found' message will be displayed.
        """
        # Cannot automate

    def test_003_based_on_pre_condition_2_navigate_to_sports_landing_page_gt_matches_tab(self):
        """
        DESCRIPTION: Based on Pre-Condition 2 Navigate to Sports Landing Page-&gt; Matches tab.
        EXPECTED: Desktop:
        EXPECTED: * 'No events Found' message will be displayed.
        EXPECTED: Mobile:
        EXPECTED: * Events shown beyond 72h along with Time frame.
        """
        # Covered in above steps

    def test_004_based_on_pre_condition_2_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Based on Pre-Condition 2 Navigate to Competitions page.
        EXPECTED: * Events shown beyond 72h along with Time frame.
        """
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='cricket')
        no_events = self.site.contents.tab_content.has_no_events_label()
        self.assertFalse(no_events, msg=f'"No Events Found" msg not displayed')

    def test_005_based_on_pre_condition_3_navigate_to_sports_landing_page_gt_matches_tab(self):
        """
        DESCRIPTION: Based on Pre-Condition 3 Navigate to Sports Landing Page-&gt; Matches tab.
        EXPECTED: Desktop:
        EXPECTED: * Time frame going to display if events are available in Today's tab.
        EXPECTED: Mobile:
        EXPECTED: * Time Frame going to displays according to the Time filters & League Filters configurations in CMS
        """
        self.test_004_based_on_pre_condition_2_navigate_to_competitions_page()
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        self.assertTrue(has_time_filter, msg='Time filter not available')

    def test_006_based_on_pre_condition_3_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Based on Pre-Condition 3 Navigate to Competitions page.
        EXPECTED: * Time Frame going to displays according to the Time filters configurations in CMS
        """
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.cricket_config.category_id)
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{expected_tab_name}"')
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        self.assertTrue(has_time_filter, msg='Time filter not available')

    def test_007_based_on_pre_condition_4_navigate_to_sports_landing_page_gt_matches_tab(self):
        """
        DESCRIPTION: Based on Pre-Condition 4 Navigate to Sports Landing Page-&gt; Matches tab.
        EXPECTED: Desktop:
        EXPECTED: * Time frame going to display if events are available in Today's tab.
        EXPECTED: Mobile:
        EXPECTED: * Time Frame going to displays according to the Time filters & League Filters configurations in CMS
        """
        # Covered in step 5

    def test_008_repeat_step_1_7_for_tier_2_sport(self):
        """
        DESCRIPTION: Repeat step 1-7 for tier-2 sport.
        EXPECTED:
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football', timeout=10)
        has_time_filter = self.site.sports_page.tab_content.has_timeline_filters()
        self.assertTrue(has_time_filter, msg='Time filter not available')
        no_events = self.site.contents.tab_content.has_no_events_label()
        self.assertFalse(no_events, msg=f'"No Events Found" msg not displayed')
        self.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.filter = list(self.filters.values())
        self.filter_name = list(self.filters.keys())
        self.assertIn(vec.bma.INVALID_LEAGUE, self.filter_name, msg=f'"{vec.bma.INVALID_LEAGUE}" not contain '
                                                                    f'"{self.filter_name}"')
        self.filter[2].click()
        selected_filters = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())
        self.assertIn(self.filter_name[2], selected_filters,
                      msg=f'Actual "{self.filter_name[2]}" is not same as expected "{selected_filters}"')

import pytest
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.time_league_filters
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.desktop
@vtest
class Test_C63943057_Verify_GA_tracking_for_the_selection_of_Time_Filters_on_the_Competitions_Page_for_Tier_1_sports(BaseDataLayerTest):
    """
    TR_ID: C63943057
    NAME: Verify GA tracking for the selection of Time Filters on the Competitions Page for Tier 1 sports
    DESCRIPTION: This Test Case verifies Time Filters GA tracking on the Competitions Page for the Tier 1 sports.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def navigate_to_league(self, league_category, league_name):

        if tests.settings.backend_env != 'prod':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[
                vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(competitions, msg='No competitions are present on page')


        category = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(league_category)
        self.assertTrue(category, msg='category is not displayed')
        if not category.is_expanded():
            category.expand()
        league = category.items_as_ordered_dict.get(league_name)
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage', timeout=30)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
        PRECONDITIONS: The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages &gt; Sport Categories &gt; Tier 1 Sport &gt; Competitions Tab )
        PRECONDITIONS: SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
        PRECONDITIONS: Access the application in the browser and click on the inspect option. Select the Console option.
        """

        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')
            self.ob_config.add_autotest_premier_league_football_event()
            self.ob_config.add_football_event_to_england_championship()

        self.cms_config.update_sports_event_filters(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
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

    def test_001_navigate_to_tier_1___sports_landing_page___competitions_tab(self):
        """
        DESCRIPTION: Navigate to Tier 1 - Sports Landing page - Competitions tab.
        EXPECTED: Time Filters Component is displayed with the following time frames: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        EXPECTED: Filters are not selected or highlighted by default
        EXPECTED: For Desktop:
        EXPECTED: Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        EXPECTED: Filters are not selected or highlighted by default
        """
        if tests.settings.backend_env != 'prod':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[
                vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(competitions, msg='No competitions are present on page')

            if self.brand == 'ladbrokes':
                league = 'Auto Test'
                self.navigate_to_league(league_category=league,
                                        league_name=vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME)
            else:
                league = 'AUTO TEST'
                self.navigate_to_league(league_category=league, league_name=vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME)
        else:
            if self.brand == 'ladbrokes':
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(),
                                        league_name=vec.siteserve.PREMIER_LEAGUE_NAME)
            else:
                self.navigate_to_league(league_category=vec.siteserve.ENGLAND,
                                        league_name=vec.siteserve.PREMIER_LEAGUE_NAME)

    def test_002_select_any_of_the_time_filter_which_is_available(self, tfilter="12h"):
        """
        DESCRIPTION: Select any of the Time filter which is available.
        EXPECTED: In the Console tab the action of adding or selecting time filter should be tracked or captured.
        EXPECTED: Details to be captured
        EXPECTED: categoryID: "Sports Category ID"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "1h; 3h; 5h"
        EXPECTED: eventCategory: "Time filters"
        EXPECTED: eventLabel: "select"
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict[tfilter].click()
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value="time filters")
        expected_response = {'event': "trackEvent",
                             'eventCategory': "time filters",
                             'eventAction': tfilter,
                             'eventLabel': "select",
                             'categoryID': "16",
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_003_deselect_the_previously_selected_time_filter(self, tfilter="12h"):
        """
        DESCRIPTION: Deselect the previously selected Time filter.
        EXPECTED: In the Console tab the action of de-selecting time filter should be tracked or captured.
        EXPECTED: Details to be captured
        EXPECTED: categoryID: "Sports Category ID"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "1h; 3h; 5h"
        EXPECTED: eventCategory: "Time filters"
        EXPECTED: eventLabel: "deselect"
        """
        self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict[tfilter].click()
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value="time filters")
        expected_response = {'event': "trackEvent",
                             'eventCategory': "time filters",
                             'eventAction': tfilter,
                             'eventLabel': "deselect",
                             'categoryID': "16",
                             }
        self.compare_json_response(actual_response, expected_response)

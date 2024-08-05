import pytest
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.time_league_filters
@pytest.mark.reg156_fix
@vtest
class Test_C63941943_Verify_GA_tracking_for_the_selection_of_League_Filters_on_the_Sports_Landing_Page(BaseDataLayerTest):
    """
    TR_ID: C63941943
    NAME: Verify GA tracking  for the selection of League Filters on the Sports Landing Page
    DESCRIPTION: This Test Case verifies League Filters GA tracking on the Sports Landing Page
    PRECONDITIONS: 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: Access the application in the browser and click on the inspect option. Select the Console option.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
        PRECONDITIONS: The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
        PRECONDITIONS: SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
        """
        self.__class__.sport_id = self.ob_config.tennis_config.category_id
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.sport_id,
                                                         number_of_events=2)
            topleagues = [events[0]['event']['typeId']]
            testleague = [events[1]['event']['typeId']]
        else:
            event_params = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=1))

            event_params2 = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=2))

            topleagues = [event_params.ss_response['event']['typeId']]
            testleague = [event_params2.ss_response['event']['typeId']]

        self.cms_config.update_sports_event_filters(tab_name='matches',
                                                    sport_id=self.sport_id, enabled=True,
                                                    league_required=True,
                                                    top_league_ids=topleagues, test_league_ids=testleague,
                                                    invalid_league_ids=[1234])

    def test_001_navigate_to_the_sports_landing_page(self, sport_name='tennis'):
        """
        DESCRIPTION: Navigate to the Sports Landing Page.
        EXPECTED: League Filters Component is displayed with the following filters: 'Top Leagues', 'Test League', 'Invalid League'
        EXPECTED: Filters are not selected or highlighted by default.
        """
        self.navigate_to_page(name='sport/' + sport_name)
        response = self.cms_config.get_sports_tab_data(sport_id=self.sport_id, tab_name='matches')
        self.__class__.filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        for item in response['filters']['league']['values']:
            self.assertIn(item.get('leagueName'), self.filters.keys(), msg=f'league value not present in ui')
        selected_filter = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertEquals(selected_filter, None, msg='League filter is selected')

    def test_002_select_any_of_the_league_filter_which_is_available(self):
        """
        DESCRIPTION: Select any of the League filter which is available.
        EXPECTED: In the Console tab the action of adding or selecting League filter should be tracked or captured.
        EXPECTED: Details to be captured
        EXPECTED: categoryID: "Sports Category ID"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "League Filter"
        EXPECTED: eventCategory: "League filters"
        EXPECTED: eventLabel: "select"
        """
        self.__class__.filter_name, self.__class__.filter = list(self.filters.items())[0]
        self.filter.click()
        expected_response = {
            "event": "trackEvent",
            "eventCategory": "time filters",
            "eventAction": self.filter_name,
            "eventLabel": "select",
            "categoryID": str(self.sport_id)
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='time filters')
        self.compare_json_response(actual_response, expected_response)

    def test_003_deselect_the_previously_selected_league_filter(self):
        """
        DESCRIPTION: Deselect the previously selected League filter.
        EXPECTED: In the Console tab the action of de-selecting League filter should be tracked or captured.
        EXPECTED: Details to be captured
        EXPECTED: categoryID: "Sports Category ID"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "League Filter"
        EXPECTED: eventCategory: "League filters"
        EXPECTED: eventLabel: "deselect"
        """
        self.filter.click()
        expected_response = {
            "event": "trackEvent",
            "eventCategory": "time filters",
            "eventAction": self.filter_name,
            "eventLabel": "deselect",
            "categoryID": str(self.sport_id)
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='time filters')
        self.compare_json_response(actual_response, expected_response)

    def test_004_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        self.__class__.sport_id = self.ob_config.cricket_config.category_id
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.sport_id,
                                                         number_of_events=2)
            topleagues = [events[0]['event']['typeId']]
            testleague = [events[1]['event']['typeId']]

        else:
            event_params = self.ob_config.add_autotest_cricket_event(
                start_time=self.get_date_time_formatted_string(hours=1))

            event_params1 = self.ob_config.add_autotest_cricket_event(
                start_time=self.get_date_time_formatted_string(hours=1))

            topleagues = [event_params.ss_response['event']['typeId']]
            testleague = [event_params1.ss_response['event']['typeId']]

        self.cms_config.update_sports_event_filters(tab_name='matches',
                                                    sport_id=self.sport_id, enabled=True,
                                                    league_required=True,
                                                    top_league_ids=topleagues, test_league_ids=testleague,
                                                    invalid_league_ids=[1234])
        self.navigate_to_page(name='home')
        self.site.wait_content_state('HomePage')
        self.test_001_navigate_to_the_sports_landing_page(sport_name='cricket')
        self.test_002_select_any_of_the_league_filter_which_is_available()
        self.test_003_deselect_the_previously_selected_league_filter()

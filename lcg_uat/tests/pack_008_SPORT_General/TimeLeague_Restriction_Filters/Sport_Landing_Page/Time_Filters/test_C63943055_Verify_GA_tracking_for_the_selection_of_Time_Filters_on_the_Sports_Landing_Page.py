import pytest
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.time_league_filters
@pytest.mark.navigation
@pytest.mark.desktop
@vtest
class Test_C63943055_Verify_GA_tracking_for_the_selection_of_Time_Filters_on_the_Sports_Landing_Page(BaseDataLayerTest):
    """
    TR_ID: C63943055
    NAME: Verify GA tracking for the selection of Time Filters on the Sports Landing Page
    DESCRIPTION: This Test Case verifies Time Filters GA tracking on the Sports Landing Page
    PRECONDITIONS: 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: Access the application in the browser and click on the inspect option. Select the Console option.
    """
    keep_browser_open = True

    def verify_time_filter_cms(self, Tier='Tier1', category_id=None):
        if Tier == 'Tier2':
            self.__class__.category_id = category_id

        self.__class__.matches_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches
        tab_data = self.cms_config.get_sports_tab_data(sport_id=self.category_id, tab_name=self.matches_tab)
        try:
            if tab_data['enabled']:
                self.__class__.time_filter_value = tab_data['filters']['time']['values']
            else:
                self.cms_config.update_sports_event_filters(tab_name=self.matches_tab,
                                                            sport_id=self.football_category_id, enabled=True,
                                                            league_required=True,
                                                            event_filters_values=[1, 3, 6, 12, 24, 48, 72])
        except Exception:
            self.cms_config.update_sports_event_filters(tab_name=self.matches_tab, sport_id=self.category_id,
                                                        enabled=True,
                                                        league_required=True,
                                                        event_filters_values=[1, 3, 6, 12, 24, 48, 72])

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
        PRECONDITIONS: The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
        PRECONDITIONS: SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
        PRECONDITIONS: Access the application in the browser and click on the inspect option. Select the Console option.
        """
        self.__class__.category_id = self.ob_config.tennis_config.category_id
        if tests.settings.backend_env == 'prod':
            self.get_active_events_for_category(category_id=self.category_id)
        else:
            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=1))
            self.ob_config.add_basketball_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(hours=1))

        self.verify_time_filter_cms(category_id=self.category_id)

    def test_001_navigate_to_sports_landing_page(self, sports='tennis'):
        """
        DESCRIPTION: Navigate to Sports Landing page
        EXPECTED: For Mobile:
        EXPECTED: Time Filters Component is displayed with the following time frames: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        EXPECTED: Filters are not selected or highlighted by default
        EXPECTED: For Desktop:
        EXPECTED: Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        EXPECTED: Filters are not selected or highlighted by default
        """
        self.navigate_to_page(name='sport/' + sports)
        self.site.wait_content_state(sports)
        expected_tab_name = self.get_sport_tab_name(self.matches_tab,
                                                    self.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        if current_tab_name != expected_tab_name:
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
            current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='Time/league filters is not displayed')
        selected_filters = self.site.sports_page.tab_content.timeline_filters.selected_filters
        self.assertFalse(selected_filters,
                         msg='Filters is selected by default, whereas it should not select by default')

    def test_002_select_any_of_the_time_filter_which_is_available(self):
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
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        filter_value = ''
        for filter_name, filter in filters.items():
            if str(self.time_filter_value[0]) == filter_name.replace('h', ''):
                filter.click()
                filter_value = filter_name
                break

        expected_track_event = {'event': 'trackEvent', 'eventCategory': 'time filters', 'eventAction': filter_value,
                                'eventLabel': 'select', 'categoryID': str(self.category_id)}

        actual_track_event_response = self.get_data_layer_specific_object(object_key='event', object_value='trackEvent')
        self.compare_json_response(actual_track_event_response, expected_track_event)

    def test_003_deselect_the_previously_selected_time_filter(self):
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
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg=' Time Filters are not present under matches tab')

        filter_value = ''
        for filter_name, filter in filters.items():
            if str(self.time_filter_value[0]) == filter_name.replace('h', ''):
                filter.click()
                filter_value = filter_name
                break

        expected_track_event = {'event': 'trackEvent', 'eventCategory': 'time filters', 'eventAction': filter_value,
                                'eventLabel': 'deselect', 'categoryID': str(self.category_id)}

        actual_track_event_response = self.get_data_layer_specific_object(object_key='event', object_value='trackEvent')
        self.compare_json_response(actual_track_event_response, expected_track_event)

    def test_004_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        if tests.settings.backend_env == 'prod':
            count = 0
            for sports in ['basketball', 'american-football']:
                if sports == "basketball":
                    self.__class__.category_id = self.ob_config.basketball_config.category_id
                else:
                    self.__class__.category_id = self.ob_config.american_football_config.category_id
                try:
                    events = self.get_active_events_for_category(category_id=self.category_id,
                                                                 number_of_events=1)
                except SiteServeException:
                    continue
                if events:
                    self.verify_time_filter_cms(category_id=self.category_id)
                    self.test_001_navigate_to_sports_landing_page(sports=sports)
                    self.test_002_select_any_of_the_time_filter_which_is_available()
                    self.test_003_deselect_the_previously_selected_time_filter()
                    count = +1
                    break
            if count == 0:
                raise SiteServeException(
                    'There are no available events for tier-2 sports  American football & Baseball')
        else:
            self.__class__.category_id = self.ob_config.basketball_config.category_id
            self.verify_time_filter_cms(Tier='Tier2', category_id=self.category_id)
            self.test_001_navigate_to_sports_landing_page(sports='basketball')
            self.test_002_select_any_of_the_time_filter_which_is_available()
            self.test_003_deselect_the_previously_selected_time_filter()

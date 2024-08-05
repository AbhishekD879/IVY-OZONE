import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #Events with specific markets cannot be found or created in prod/Beta
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089519_Verify_pre_selected_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Basketball(BaseDataLayerTest):
    """
    TR_ID: C60089519
    NAME: Verify pre selected ‘WW’ MT is saved when switching b/w T/T/F on Matches Tab for Basketball
    DESCRIPTION: This test case verifies that previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Basketball Landing Page
    PRECONDITIONS: Precondition:
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line (Win/Win)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: MR
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the basketball Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money line(WW)| - "Money line"
    """
    keep_browser_open = True

    days_list = [vec.sb.TABS_NAME_TOMORROW.upper(),
                 vec.sb.TABS_NAME_FUTURE.upper(),
                 vec.sb.TABS_NAME_TODAY.upper()]

    def verify_pre_selected_option_and_labels_and_GA_tracking_functionality_for_tab(self, tab):
        if self.device_type == 'desktop':
            req_tab = tab.upper() if self.brand == 'bma' else tab.title()
            self.grouping_buttons.items_as_ordered_dict.get(req_tab).click()
            self.site.wait_content_state_changed()
            has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
            if has_market_selector:
                selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
                self.assertEqual(selected_value.upper(), self.expected_MS,
                                 msg=f'Actual selected value: "{selected_value}" is not same as'
                                     f'Expected selected value: "{self.expected_MS}"')
            else:
                self._logger.info(msg=f' "Market Selector" is not displayed in "{tab}" tab.')
            self.test_003_verify_displaying_of_preplay_events()
            self.test_002_verify_text_of_the_labels_for_money_line()
            self.test_004_verify_ga_tracking_for_the_money_line()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the basketball Landing page -> 'Matches' tab
        """
        self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball', status=True)
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.basketball.category_id,
            disp_sort_names='HL,WH,HH',
            primary_markets='|Money Line|,|Total Points|,'
                            '|Home team total points|,|Away team total points|,'
                            '|Half Total Points|,|Quarter Total Points|,'
                            '|Handicap 2-way|')
        self.ob_config.add_basketball_event_to_us_league()
        tomorrow = self.get_date_time_formatted_string(days=1)
        self.ob_config.add_basketball_event_to_us_league(start_time=tomorrow)
        future = self.get_date_time_formatted_string(days=7)
        self.ob_config.add_basketball_event_to_us_league(start_time=future)

        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.basketball_config.category_id)
        self.navigate_to_page("sport/basketball")
        self.site.wait_content_state('basketball')
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed(timeout=10)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')
        if self.device_type == 'desktop':
            self.__class__.grouping_buttons = self.site.contents.tab_content.grouping_buttons
            current_tab = self.grouping_buttons.current
            self.assertEqual(current_tab.upper(), vec.sb.TABS_NAME_TODAY.upper(),
                             msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                                 f'Expected tab: "{vec.sb.TABS_NAME_TODAY.upper()}".')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Basketball')

        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                self.site.wait_content_state_changed(timeout=20)
                self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        self.__class__.expected_MS = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line.upper()
        self.assertEqual(selected_value.upper(), self.expected_MS,
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{self.expected_MS}"')

    def test_002_verify_text_of_the_labels_for_money_line(self):
        """
        DESCRIPTION: Verify text of the labels for 'Money Line'
        EXPECTED: • The events for the Money Line market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        # covered in step 3

    def test_003_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        self.__class__.leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(self.leagues) > 0:
            fixture = self.leagues[0].fixture_header
            self.assertEqual(fixture.header1, '1',
                             msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                                 f'Expected "{1}"')
            self.assertEqual(fixture.header3, '2',
                             msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                                 f'Expected "{2}"')

            for league in self.leagues:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    odds = list(event.template.items_as_ordered_dict.values())
                    for odd in odds:
                        self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                    self.assertFalse(event.template.is_live_now_event,
                                     msg=f'Event: "{event}" is not a "Preplay" Event')
        else:
            no_events = self.site.contents.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_004_verify_ga_tracking_for_the_money_line(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Money Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Money Line"
        EXPECTED: categoryID: "6"
        EXPECTED: })
        """
        if len(self.leagues) > 0:
            self.dropdown = self.site.contents.tab_content.dropdown_market_selector
            self.dropdown.click_item(self.expected_MS)
            actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Money Line')
            expected_response = {'event': 'trackEvent',
                                 'eventCategory': 'market selector',
                                 'eventAction': 'change market',
                                 'eventLabel': 'Money Line',
                                 'categoryID': 6,
                                 }
            self.compare_json_response(actual_response, expected_response)

    def test_005_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Money Line)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        self.verify_pre_selected_option_and_labels_and_GA_tracking_functionality_for_tab(tab=self.days_list[0])

    def test_006_repeat_steps_34(self):
        """
        DESCRIPTION: Repeat steps 3,4
        EXPECTED:
        """
        # covered in step 5

    def test_007_repeat_steps_345_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4,5 for the 'Future' tab
        EXPECTED:
        """
        self.verify_pre_selected_option_and_labels_and_GA_tracking_functionality_for_tab(tab=self.days_list[1])

    def test_008_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        self.verify_pre_selected_option_and_labels_and_GA_tracking_functionality_for_tab(tab=self.days_list[2])

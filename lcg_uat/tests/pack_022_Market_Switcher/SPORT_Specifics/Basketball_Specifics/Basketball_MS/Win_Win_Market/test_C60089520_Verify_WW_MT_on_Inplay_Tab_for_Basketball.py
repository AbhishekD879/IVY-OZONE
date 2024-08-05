import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #Events with specific markets cannot be found or created in prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089520_Verify_WW_MT_on_Inplay_Tab_for_Basketball(BaseDataLayerTest, BaseSportTest):
    """
    TR_ID: C60089520
    NAME: Verify 'WW’ MT on Inplay Tab for Basketball
    DESCRIPTION: This test case verifies displaying of ‘WW market’ Template is displaying by default for Basketball Landing Page on Inplay Tab under Market Selector Dropdown
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Basketball ->Inplay Tab and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money line(WW)| - "Money line"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create basketball event with required markets
        EXPECTED: Event is successfully created
        """
        all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sport')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
        start_time = self.get_date_time_formatted_string(seconds=20)
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.basketball.category_id,
            disp_sort_names='HL,WH,HH',
            primary_markets='|Money Line|,|Total Points|,'
                            '|Home team total points|,|Away team total points|,'
                            '|Half Total Points|,|Quarter Total Points|,'
                            '|Handicap 2-way|')
        self.ob_config.add_basketball_event_to_us_league(is_live=True,
                                                         start_time=start_time)
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        expected_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play
        self.site.basketball.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        expected_tab_name = self.get_sport_tab_name(expected_tab, self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: * The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: Desktop:
        EXPECTED: * The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change Market' button is placed next to 'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: * 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        has_market_selector = self.site.basketball.tab_content.has_dropdown_market_selector()
        dropdown = self.site.basketball.tab_content.dropdown_market_selector
        dropdown.scroll_to()
        self.site.wait_content_state_changed()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Basketball')

        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.site.inplay.tab_content.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.assertTrue(dropdown.change_market_button, msg=f'"Change button" is not displayed')
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        if self.device_type == 'desktop' and self.brand == 'ladbrokes':
            selected_value = self.site.contents.tab_content.selected_market
        else:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_item.rstrip()
        expected_MS = vec.siteserve.EXPECTED_MARKETS_NAMES.main_markets.upper()
        self.assertEqual(selected_value.upper(), expected_MS,
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{expected_MS}"')

    def test_002_verify_text_of_the_labels_for_money_line(self):
        """
        DESCRIPTION: Verify text of the labels for 'Money Line'
        EXPECTED: • The events for the Money Line market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        # covered in step 3

    def test_003_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        self.site.wait_content_state_changed()
        leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(leagues) > 0:
            fixture = leagues[0].fixture_header
            self.assertEqual(fixture.header1, '1',
                             msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                                 f'Expected "{1}"')
            self.assertEqual(fixture.header3, '2',
                             msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                                 f'Expected "{2}"')

            for league in leagues:
                self.site.wait_content_state_changed()
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    odds = list(event.template.items_as_ordered_dict.values())
                    for odd in odds:
                        self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                    self.assertTrue(event.template.is_live_now_event,
                                    msg=f'Event: "{event}" is not a "Preplay" Event')
        else:
            no_events = self.site.contents.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_004_verify_displaying_of_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Inplay events
        EXPECTED: Only Inplay events should be displayed
        """
        # covered in step 3

    def test_005_verify_ga_tracking_for_the_money_line(self):
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
        if self.device_type == 'desktop' and self.brand == 'bma':
            selector = self.site.basketball.tab_content.dropdown_market_selector
            selector.scroll_to()
            selector.value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
            actual = self.site.basketball.tab_content.dropdown_market_selector.value.rstrip()
        else:
            selector = self.site.inplay.tab_content.dropdown_market_selector
            selector.scroll_to()
            selector.value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
            self.site.wait_content_state_changed()
            actual = self.site.inplay.tab_content.selected_market
        self.assertEqual(actual.rstrip(), vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                         msg=f'Selected market selector "{actual}" is not the same as expected "{vec.siteserve.EXPECTED_MARKETS_NAMES.money_line}"')
        self.site.basketball.tab_content.dropdown_market_selector.scroll_to()
        self.expected_market_selector_response['categoryID'] = self.ob_config.backend.ti.basketball.category_id
        self.expected_market_selector_response['eventLabel'] = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                              object_value='change market')
        self.compare_json_response(actual_response, self.expected_market_selector_response)

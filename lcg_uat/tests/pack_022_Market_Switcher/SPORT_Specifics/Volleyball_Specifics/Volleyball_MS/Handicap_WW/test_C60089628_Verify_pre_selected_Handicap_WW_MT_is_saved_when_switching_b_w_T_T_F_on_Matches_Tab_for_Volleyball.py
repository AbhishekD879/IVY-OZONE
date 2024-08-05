import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60089628_Verify_pre_selected_Handicap_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Volleyball(BaseDataLayerTest):
    """
    TR_ID: C60089628
    NAME: Verify pre selected ‘Handicap WW’ MT is saved when switching b/w T/T/F on Matches Tab for Volleyball
    DESCRIPTION: This test case verifies that previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Volleyball Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Total Points|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Volleyball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Set Handicap (Handicap)| - "Set Handicap"
    PRECONDITIONS: * |Total Match Points (Over/Under)| - "Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    handicap_market = True
    markets = [('total_match_points', {'handicap': 2}),
               ('total_match_points_2', {'handicap': 3}),
               ('match_set_handicap_2', {'handicap': 3})]
    total_match_points_expected_handicap_value = 2
    match_set_handicap_expected_handicap_value = 5

    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.total_match_points]

    def verify_market_event_fixture(self):
        self.__class__.leagues = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(self.leagues) > 0:
            selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
            if selected_value.upper() == self.expected_list[0].upper():
                header_1 = '1'
                header_2 = '2'
            else:
                header_1 = vec.sb.FIXTURE_HEADER.over
                header_2 = vec.sb.FIXTURE_HEADER.under

            fixture = self.leagues[0].fixture_header
            self.assertEqual(fixture.header1, header_1,
                             msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{header_1}"')
            self.assertEqual(fixture.header3, header_2,
                             msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{header_2}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate volleybal landing page
        EXPECTED: Event is successfully created
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='volleyball', status=True)
        self.assertTrue(status, msg=f'The sport "volleyball" is not checked')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.volleyball_config.category_id,
                                                       disp_sort_names='HH,MH,WH,HL,3W',
                                                       primary_markets='|Match Betting|,|Handicap Match Result|,|Match Set Handicap|,|Total Match Points|,|Set X Winner||Handicap 3-Way|')

        event = self.ob_config.add_volleyball_event_to_austrian_league_avl_set_handicap(markets=self.markets, disp_order=2)
        self.__class__.event_name = event.team1 + ' v ' + event.team2
        self.navigate_to_page(name='sport/volleyball')
        self.site.wait_content_state('volleyball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.volleyball_config.category_id)
        self.site.sports_page.tabs_menu.click_button(expected_tab_name)
        current_tab = self.site.sports_page.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')
        self.__class__.grouping_buttons = self.site.contents.tab_content.grouping_buttons
        current_tab = self.grouping_buttons.current
        self.assertEqual(current_tab.upper(), vec.sb.TABS_NAME_TODAY.upper(),
                         msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                         f'Expected tab: "{vec.sb.TABS_NAME_TODAY.upper()}".')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Set Handicap' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Set Handicap' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Set Handicap' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for volleyball')
        self.__class__.dropdown = self.site.sports_page.tab_content.dropdown_market_selector
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
                wait_for_result(lambda: self.dropdown.is_expanded() is not True,
                                name=f'Market switcher expanded/collapsed',
                                timeout=5)
                self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap.upper(),
                             msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap.upper()}"')
        except VoltronException:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap).click()

    def test_002_select_set_handicap_in_the_market_selector_dropdown_list(self, market=expected_list[0], handicap_value=match_set_handicap_expected_handicap_value):
        """
        DESCRIPTION: Select 'Set Handicap' in the 'Market Selector' dropdown list
        EXPECTED: • Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        EXPECTED: Note- When multiple markets are created for the any handicap market , then user should be able to see one market for each market type in landing page and in EDP page whole list will be displayed with all the different handicap values for that particular market.
        """
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        self.__class__.leagues = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')
        for league in self.leagues:
            if not league.is_expanded():
                league.expand()
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                if self.event_name == event_template.event_name:
                    handicap = event_template.items_names
                    handicap_values = list(event_template.items_as_ordered_dict.values())
                    for val in handicap_values:
                        self.assertEqual(val.handicap_value.text_color_value, vec.colors.HANDICAP_COLOR,
                                         msg=' "Handicap Value" is not in blue color')
                    for value in handicap:
                        actual_value = value.split('\n')[0]
                        self.assertIn(str(handicap_value), actual_value,
                                      msg=f'{handicap_value} value is not displayed as per dispsort value ')
                        if self.handicap_market:
                            if int(float(actual_value)) >= 0:
                                self.assertNotIn('-', actual_value,
                                                 msg=' "Negative value" present in button')
                            else:
                                self.assertIn('-', actual_value,
                                              msg=' "Negative value" not present in button')
                        else:
                            self.assertNotIn('-', actual_value,
                                             msg=' "Negative value" present in button')

    def test_003_verify_text_of_the_labels_for_set_handicap_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Set Handicap' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        self.verify_market_event_fixture()

    def test_004_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        self.__class__.leagues = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(self.leagues) > 0:
            for league in self.leagues:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    self.assertFalse(event.template.is_live_now_event,
                                     msg=f'Event: "{event}" is an "In-Play" Event')
                    self.assertTrue(event.template.event_name, msg=' "Event Name" not displayed')
                    self.assertTrue(event.template.event_time, msg=' "Event time" not displayed')
                    self.assertTrue(event.template.has_markets, msg='There is no "More" markets link')
                    self._logger.info(f'Only preplay events found in league:"{league}"')
        else:
            self._logger.info(msg=' "No events found".')
            has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
            self.assertFalse(has_market_selector, msg=' "Market Selector" is displayed" ')

    def test_005_verify_ga_tracking_for_the_set_handicap(self, market=expected_list[0]):
        """
        DESCRIPTION: Verify GA Tracking for the 'Set Handicap'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Set Handicap"
        EXPECTED: categoryID: "36"
        EXPECTED: })
        """
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        if self.brand == 'ladbrokes':
            selected_value = selected_value.title()
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=selected_value)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': selected_value,
                             'categoryID': 36,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_006_switch_to_the_tomorrow_tab(self, market=expected_list[0]):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Set Handicap)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label 1&2
        EXPECTED: Note:
        EXPECTED: If events are not present for Set Handicap market and if events are present for Total Points market then Total Points will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        if self.brand == 'bma':
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.upper(),
                                        vec.sb.TABS_NAME_FUTURE.upper(),
                                        vec.sb.TABS_NAME_TODAY.upper()]
        else:
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.title(),
                                        vec.sb.TABS_NAME_FUTURE.title(),
                                        vec.sb.TABS_NAME_TODAY.title()]

        self.grouping_buttons.items_as_ordered_dict.get(self.days_list[0]).click()
        self.site.wait_content_state_changed()
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_value.upper(), market.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{market}"')
        else:
            self.assertFalse(has_market_selector, msg=' "Market Selector" is displayed" ')
        self.verify_market_event_fixture()
        self.test_004_verify_displaying_of_preplay_events()

    def test_007_repeat_steps_345(self):
        """
        DESCRIPTION: Repeat steps 3,4,5
        """
        # 3, 4 steps covered in step 6
        if len(self.leagues) > 0:
            self.test_005_verify_ga_tracking_for_the_set_handicap()

    def test_008_repeat_steps_345_for_the_future_tab(self, market=expected_list[0]):
        """
        DESCRIPTION: Repeat steps 3,4,5 for the 'Future' tab
        """
        self.grouping_buttons.items_as_ordered_dict.get(self.days_list[1]).click()
        self.site.wait_content_state_changed()
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_value.upper(), market.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{market}"')
        else:
            self.assertFalse(has_market_selector, msg=' "Market Selector" is displayed" ')
        self.test_003_verify_text_of_the_labels_for_set_handicap_in_matches_tab()
        if len(self.leagues) > 0:
            self.test_005_verify_ga_tracking_for_the_set_handicap()

    def test_009_switch_back_to_today_tab(self, market=expected_list[0]):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label 1&2
        """
        self.grouping_buttons.items_as_ordered_dict.get(self.days_list[2]).click()
        self.site.wait_content_state_changed()
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_value.upper(), market.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{market}"')
        else:
            self.assertFalse(has_market_selector, msg=' "Market Selector" is displayed" ')
        self.test_003_verify_text_of_the_labels_for_set_handicap_in_matches_tab()

    def test_010_repeat_steps_2_9_for_below_markettotal_points_expect_step3(self):
        """
        DESCRIPTION: Repeat steps 2-9 for below market
        DESCRIPTION: Total Points (expect step3)
        """
        self.__class__.handicap_market = False
        self.test_002_select_set_handicap_in_the_market_selector_dropdown_list(market=self.expected_list[1], handicap_value=self.total_match_points_expected_handicap_value)
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_set_handicap(market=self.expected_list[1])
        self.test_006_switch_to_the_tomorrow_tab(market=self.expected_list[1])
        self.test_007_repeat_steps_345()
        self.test_008_repeat_steps_345_for_the_future_tab(market=self.expected_list[1])
        self.test_009_switch_back_to_today_tab(market=self.expected_list[1])

    def test_011_verify_text_of_the_labels_for_total_points_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        """
        self.test_003_verify_text_of_the_labels_for_set_handicap_in_matches_tab()
